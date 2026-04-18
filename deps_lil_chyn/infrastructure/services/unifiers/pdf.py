import logging
import multiprocessing
from dataclasses import dataclass
from io import BytesIO
from multiprocessing import Process, Queue
from queue import Empty
from typing import Any

from deps_object_storage import ObjectStorage, make_object_storage
from deps_unified_data.model import Bbox, UnifiedData, UnifiedDataFactory, WordBox

from deps_lil_chyn.constants import DEFAULT_PDF_MAX_PROCESSES, DEFAULT_TARGET_DPI
from deps_lil_chyn.domain.dto import FileData, ImageData
from deps_lil_chyn.domain.services import PdfToImagesConverter, VectorPdfExtractor
from deps_lil_chyn.domain.services.vector_pdf_extractor import Page

from .abstract_unifier import AbstractUnifier

logger = logging.getLogger(__name__)

Confidence = float
Content = str

__all__ = ["PdfUnifier"]


@dataclass
class PageTask:
    page_index: int
    image_data: ImageData
    wordboxes: list[WordBox]
    file_name: str


class PdfUnifier(AbstractUnifier):
    extensions: set[str] = {"pdf"}

    def __init__(
        self,
        object_storage: ObjectStorage,
        vector_pdf_extractor: VectorPdfExtractor,
        target_dpi: int = DEFAULT_TARGET_DPI,
        max_processes: int = DEFAULT_PDF_MAX_PROCESSES,
    ) -> None:
        super().__init__(object_storage=object_storage)
        self._vector_pdf_extractor = vector_pdf_extractor
        self._target_dpi = target_dpi
        self._max_processes = max_processes

    def unify(self, document_id: str, files: list[str]) -> UnifiedData:
        unified_data = UnifiedDataFactory.make_unified_data(document_id)

        for file_path in files:
            self._unify_file(unified_data, file_path)

        return unified_data

    def _unify_file(self, unified_data: UnifiedData, file_path: str) -> None:
        logger.info(
            f"Downloading source file for document `{unified_data.document_id}` from `{file_path}`"
        )

        file_data, page_wordboxes = self._prepare_input(file_path)
        results = self._run_processing_pool(file_data, page_wordboxes)
        self._build_unified_data(unified_data, results)

    def _prepare_input(
        self, file_path: str
    ) -> tuple[FileData, dict[Page, list[WordBox]]]:
        file_data = self._download_file_from_storage(file_path)
        with BytesIO(file_data.content) as file_stream:
            page_wordboxes = self._vector_pdf_extractor.extract_wordboxes(file_stream)

        return file_data, page_wordboxes

    def _run_processing_pool(
        self,
        file_data: FileData,
        page_wordboxes: dict[Page, list[WordBox]],
    ) -> list[dict[str, Any]]:
        task_queue: Queue = multiprocessing.Queue(maxsize=self._max_processes * 2)
        result_queue: Queue = multiprocessing.Queue()

        def worker(task_q: Queue, result_q: Queue):
            object_storage = make_object_storage()
            while True:
                task: PageTask = task_q.get()
                if task is None:
                    break

                logger.info(
                    f"[PID={multiprocessing.current_process().pid}] Processing page {task.page_index + 1}"
                )

                img_file = FileData(
                    path=self._get_original_image_path(
                        task.file_name, f"{task.page_index}.png"
                    ),
                    content=task.image_data.content,
                )

                blob_name = object_storage.upload(
                    path=img_file.path,
                    content=img_file.content,
                    replace_if_exists=True,
                )

                result_q.put(
                    {
                        "page_index": task.page_index,
                        "blob_name": blob_name,
                        "width": task.image_data.shape.width,
                        "height": task.image_data.shape.height,
                        "wordboxes": self._wordboxes_to_tuples(task.wordboxes),
                    }
                )

        # start worker pool
        workers = [
            Process(target=worker, args=(task_queue, result_queue))
            for _ in range(self._max_processes)
        ]
        for w in workers:
            w.start()

        # producer: stream pages lazily
        with BytesIO(file_data.content) as file_stream:
            for page_index, image_data in enumerate(
                PdfToImagesConverter.convert(file=file_stream, dpi=self._target_dpi)
            ):
                task_queue.put(
                    PageTask(
                        page_index=page_index,
                        image_data=image_data,
                        wordboxes=page_wordboxes.get(page_index, []),
                        file_name=file_data.name,
                    )
                )

        # tell workers to exit
        for _ in workers:
            task_queue.put(None)

        # collect results
        results = []
        total_pages = len(page_wordboxes)
        finished = 0
        while finished < total_pages:
            try:
                r = result_queue.get()
                results.append(r)
                finished += 1
            except Empty:
                break

        for w in workers:
            w.join()

        return results

    def _build_unified_data(
        self,
        unified_data: UnifiedData,
        results: list[dict[str, Any]],
    ) -> None:
        for r in sorted(results, key=lambda x: x["page_index"]):
            image = (
                unified_data.image_builder.for_page(r["page_index"] + 1)
                .with_blob(r["blob_name"])
                .with_shape(width=r["width"], height=r["height"])
                .build()
            )

            if r["wordboxes"]:
                (
                    unified_data.positonal_text_builder.for_page(r["page_index"] + 1)
                    .from_image(image.id.value)
                    .with_wordboxes(raw_words=r["wordboxes"])
                    .build()
                )

    @staticmethod
    def _wordboxes_to_tuples(
        wordboxes: list[WordBox],
    ) -> list[tuple[Content, Confidence, Bbox]]:
        return [
            (wordbox.word.content, wordbox.word.confidence, wordbox.bbox)
            for wordbox in wordboxes
        ]
