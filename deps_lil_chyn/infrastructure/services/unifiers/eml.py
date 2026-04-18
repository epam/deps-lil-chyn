import email
from email.message import Message
from io import BytesIO, StringIO
from typing import Optional

import mailparser
from deps_object_storage import ObjectStorage
from rtfparse.parser import Rtf_Parser
from rtfparse.renderers import de_encapsulate_html

from deps_lil_chyn.domain.dto import (
    AttachmentInfo,
    ContainerType,
    EmailMetadata,
    FileData,
    UnifiedContainerData,
)

from .abstract_container_unifier import AbstractContainerUnifier

__all__ = ["EmlUnifier"]

MULTIPART_CONTENT_TYPE = "multipart"
ATTACHMENT = "attachment"


class EmlUnifier(AbstractContainerUnifier):
    extensions: set[str] = {"eml"}

    def __init__(
        self,
        object_storage: ObjectStorage,
        supported_attachment_extensions: Optional[set[str]] = None,
    ) -> None:
        super().__init__(object_storage=object_storage)
        self.supported_attachment_extensions = supported_attachment_extensions or set()

    def unify(self, file_path: str) -> UnifiedContainerData:
        file_data = self._download_file_from_storage(file_path)
        return self._unify(file_content=file_data.content)

    def _unify(self, file_content: bytes) -> UnifiedContainerData:
        message = email.message_from_bytes(file_content)

        mail = mailparser.parse_from_bytes(file_content)
        html_body = self._convert_rtf_to_html(
            "".join(mail.text_not_managed)
        ) or "".join(mail.text_html)
        html_body = html_body.replace('""', '"')

        return UnifiedContainerData(
            container_type=ContainerType.EMAIL,
            container_metadata=EmailMetadata(
                subject=message.get("subject"),
                sender=self._get_email_sender(mail, message),
                recipients=self._get_email_recipients(mail),
                cc=(
                    [c.strip() for c in message["cc"].split(",")]
                    if message.get("cc")
                    else []
                ),
                body=html_body,
                date=str(message["date"]),
            ),
            attachments=self._get_email_attachments(message),
        )

    def _get_email_attachments(self, message: Message) -> list[AttachmentInfo]:
        attachments = []

        for part in message.walk():
            if (
                part.get_content_type() == MULTIPART_CONTENT_TYPE
                or part.get_content_disposition() != ATTACHMENT
            ):
                continue

            file_name = part.get_filename()

            if not file_name:
                continue

            file_extension = self._get_file_extension(file_name)
            unique_file_name = self._generate_unique_file_name(file_name)

            if file_extension in self.supported_attachment_extensions:
                blob_name = self._upload_file_to_storage(
                    FileData(
                        path=unique_file_name, content=part.get_payload(decode=True)  # type: ignore
                    )
                )
                attachments.append(AttachmentInfo(title=file_name, blob_name=blob_name))

        return attachments

    @staticmethod
    def _get_email_sender(mail: mailparser.MailParser, message: Message) -> str:
        if (
            len(mail.from_) > 1
        ):  # case when sender is not parsed correctly by mail-parser lib
            return (
                message["from"].split("<")[0].rstrip()
            )  # no sender email address, only name

        if mail.from_[0] and len(mail.from_[0]) == 2:
            sender_name, sender_address = mail.from_[0]
            sender = f"{sender_name} <{sender_address}>"
        else:
            sender = ""
        return sender

    @staticmethod
    def _get_email_recipients(mail: mailparser.MailParser) -> list[str]:
        recipients = mail.to
        email_recipients = set()
        for name, address in recipients:
            address = address.replace("'", "")
            recipient = f"<{address}>"
            if name:
                recipient = f"{name} {recipient}"
            email_recipients.add(recipient)
        return list(email_recipients)

    @staticmethod
    def _convert_rtf_to_html(rtf_text: str) -> Optional[str]:
        with BytesIO(bytes(rtf_text, "utf-8")) as rtf_input:
            rtf_parser = Rtf_Parser(rtf_file=rtf_input)
            try:
                parsed = rtf_parser.parse_file()
            except AttributeError:  # Raises when text is not rtf
                return None

        renderer = de_encapsulate_html.De_encapsulate_HTML()

        with StringIO() as html_output:
            renderer.render(parsed, html_output)
            return html_output.getvalue()
