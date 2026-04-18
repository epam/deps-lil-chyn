import logging
import sys
from dataclasses import asdict

from dependency_injector.wiring import Provide, inject
from deps_message_flow.commands.consumer.command_message import CommandMessage
from deps_message_flow.messaging.producer import IMessageProducer
from deps_message_flow.sagas.participant import PluginReplyBuilder

from deps_lil_chyn.application import Application
from deps_lil_chyn.containers import Containers
from deps_lil_chyn.domain.events import (
    PerformContainerUnificationReply,
    PerformUnificationReply,
)
from deps_lil_chyn.domain.exceptions import BusinessException

from .error_type import ErrorType

__all__ = ["unify_document_handler", "unify_container_document_handler"]

logger = logging.getLogger(__name__)


@inject
def unify_document_handler(
    command_message: CommandMessage,
    application_service: Application = Provide[Containers.application],
    command_producer: IMessageProducer = Provide[Containers.messaging.producer],
) -> None:
    error_type, error_message, traceback = None, None, None
    try:
        application_service.unify_document(
            document_id=command_message.command.document_id,
            files=command_message.command.files,
        )
    except BusinessException as e:
        error_type, error_message, traceback = (
            ErrorType.BUSINESS,
            str(e),
            sys.exc_info(),
        )
    except Exception as e:
        error_type, error_message, traceback = (
            ErrorType.SYSTEM,
            str(e),
            sys.exc_info(),
        )

    if error_type is not None:
        logger.error(
            f"Failed to unify {command_message.command.document_id} document! \n Reason: {error_message}",
            exc_info=traceback,
        )

    reply = PerformUnificationReply(error_type, error_message)
    destination, message = PluginReplyBuilder.for_command(command_message).with_success(
        reply
    )
    command_producer.send(destination, message)


@inject
def unify_container_document_handler(
    command_message: CommandMessage,
    application_service: Application = Provide[Containers.application],
    command_producer: IMessageProducer = Provide[Containers.messaging.producer],
) -> None:
    error_type, error_message, traceback = None, None, None
    container_type = None
    container_metadata = None
    attachments = None

    try:
        unified_container_data = application_service.unify_container_document(
            document_id=command_message.command.document_id,
            file_path=command_message.command.file_path,
        )
        container_type = unified_container_data.container_type
        container_metadata = asdict(unified_container_data.container_metadata)
        attachments = [
            asdict(attachment) for attachment in unified_container_data.attachments
        ]
    except BusinessException as e:
        error_type, error_message, traceback = (
            ErrorType.BUSINESS,
            str(e),
            sys.exc_info(),
        )
    except Exception as e:
        error_type, error_message, traceback = (
            ErrorType.SYSTEM,
            str(e),
            sys.exc_info(),
        )

    if error_type is not None:
        logger.error(
            f"Failed to unify container {command_message.command.document_id}! \n Reason: {error_message}",
            exc_info=traceback,
        )

    reply = PerformContainerUnificationReply(
        container_type=container_type,
        container_metadata=container_metadata,
        attachments=attachments,
        error_type=error_type,
        error_message=error_message,
    )

    destination, message = PluginReplyBuilder.for_command(command_message).with_success(
        reply
    )
    command_producer.send(destination, message)
