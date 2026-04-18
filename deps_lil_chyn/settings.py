from typing import Any

from deps_asb import ASBSettings
from deps_kafka import KafkaSettings
from deps_message_flow import MessagingDriverEnum
from deps_rabbitmq import RabbitMQTLSSettings
from pydantic import ConfigDict, Field, field_validator
from pydantic_settings import BaseSettings

from deps_lil_chyn.constants import DEFAULT_PDF_MAX_PROCESSES, DEFAULT_TARGET_DPI
from deps_lil_chyn.extras.settings import ServiceInfoSettings
from deps_lil_chyn.infrastructure.services import (
    CsvUnifier,
    DocUnifier,
    DocxUnifier,
    ExcelUnifier,
    ImageUnifier,
    PdfUnifier,
)


class Settings(BaseSettings):
    env: str = "development"
    default_command_channel: str | None = Field(
        None,
        validation_alias="DEFAULT_COMMAND_CHANNEL",
    )
    verify_ssl: bool = Field(True)
    api_key: str | None = Field(None)
    info: ServiceInfoSettings = ServiceInfoSettings()
    logger_level: str = Field("INFO", validation_alias="LOG_LEVEL")

    messaging_driver: MessagingDriverEnum
    messaging_driver_settings: Any = Field(
        None, validation_alias="MESSAGING_DRIVER_SETTINGS"
    )
    message_broker_connection_string: str

    file_storage_url: str
    document_type_url: str
    unifier_url: str

    cell_chunk_size: int = 100
    target_dpi: int = Field(DEFAULT_TARGET_DPI, validation_alias="TARGET_DPI")
    pdf_max_processes: int = Field(
        DEFAULT_PDF_MAX_PROCESSES, validation_alias="PDF_MAX_PROCESSES"
    )

    msg_to_eml_converter_script_path: str = Field(
        "/email-outlook-message-perl/script/msgconvert",
    )
    supported_attachment_extensions: set[str] = Field(default_factory=set)

    instrumentation_enabled: bool = Field(False)

    @classmethod
    @field_validator("messaging_driver_settings")
    def validate_messaging_driver_settings(cls, v, info):  # noqa: N805
        messaging_driver = info.data.get("messaging_driver")
        if not messaging_driver:
            raise ValueError("Invalid messaging driver")

        if messaging_driver == MessagingDriverEnum.ASB.value:
            return ASBSettings()
        elif messaging_driver == MessagingDriverEnum.KAFKA.value:
            return KafkaSettings()
        elif messaging_driver == MessagingDriverEnum.RABBITMQ.value:
            return RabbitMQTLSSettings().model_dump()  # TODO: use BaseSettings

        raise ValueError(f"Driver {messaging_driver} is not implemented")

    @classmethod
    @field_validator("supported_attachment_extensions")
    def validate_supported_attachment_extensions(cls, v: set[str]) -> set[str]:
        allowed_extensions = (
            DocUnifier.extensions
            | DocxUnifier.extensions
            | PdfUnifier.extensions
            | CsvUnifier.extensions
            | ImageUnifier.extensions
            | ExcelUnifier.extensions
        )
        for extension in v:
            if extension not in allowed_extensions:
                raise ValueError(f"Attachment extension `{extension}` is not supported")
        return v

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)
