import logging

from deps_lil_chyn.entrypoint import init_containers
from deps_lil_chyn.settings import Settings

logging.basicConfig(
    level=Settings().logger_level.upper(),
    format="[%(asctime)s] [%(name)s: %(levelname)s] %(message)s",  # noqa: WPS323
    datefmt="%Y-%m-%d %I:%M:%S",  # noqa: WPS323
)

containers = init_containers()

pdf_unifier = containers.unifiers.pdf
image_unifier = containers.unifiers.image
excel_unifier = containers.unifiers.excel
docx_unifier = containers.unifiers.docx
doc_unifier = containers.unifiers.doc
eml_unifier = containers.unifiers.eml
msg_unifier = containers.unifiers.msg
csv_unifier = containers.unifiers.csv
tiff_unifier = containers.unifiers.tiff
unifier_proxy = containers.external_services.unifier_proxy
object_storage = containers.external_services.object_storage
