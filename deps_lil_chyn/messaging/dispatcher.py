import logging

from dependency_injector.wiring import Provide, inject
from deps_message_flow.commands.consumer import (
    CommandDispatcher,
    CommandHandlersBuilder,
)
from deps_message_flow.messaging.consumer import IMessageConsumer
from deps_message_flow.messaging.producer import IMessageProducer

from deps_lil_chyn.containers import Containers
from deps_lil_chyn.domain.events import UnifyContainerDocument, UnifyDocument
from deps_lil_chyn.domain.interfaces import IUnifierPlugin

from .handlers import unify_container_document_handler, unify_document_handler

logger = logging.getLogger(__name__)


__all__ = ["run_message_dispatcher"]


@inject
def make_message_dispatcher(
    command_channel: str,
    command_queue: str,
    consumer: IMessageConsumer = Provide[Containers.messaging.consumer],
    producer: IMessageProducer = Provide[Containers.messaging.producer],
) -> IMessageConsumer:
    logger.info("Start consuming...")

    commands_handlers = (
        CommandHandlersBuilder.from_channel(command_channel)
        .on_message(UnifyDocument, unify_document_handler)
        .on_message(UnifyContainerDocument, unify_container_document_handler)
        .for_queue(command_queue)
        .build()
    )

    cd = CommandDispatcher(commands_handlers, consumer, producer)
    cd.initialize()

    return consumer


def register_command_queue(channel_name: str) -> str:
    return f"{channel_name.lower()}-unifier-queue"


@inject
def run_message_dispatcher(
    plugin: IUnifierPlugin, containers: Containers = Provide[Containers]
) -> None:
    containers.plugin.provided_by(plugin)
    command_channel = containers.application().get_command_channel(plugin)
    command_queue = register_command_queue(command_channel)
    consumer = make_message_dispatcher(
        command_channel=command_channel, command_queue=command_queue
    )

    consumer.start_consuming()  # type: ignore
