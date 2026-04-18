import logging

from deps_lil_chyn.containers import Containers
from deps_lil_chyn.infrastructure.access_management.context_vars import user
from deps_lil_chyn.messaging import dispatcher, handlers
from deps_lil_chyn.settings import Settings

logger = logging.getLogger(__name__)


def enable_auth(containers: Containers) -> None:
    containers.message_brokers.broker_client().user_context = user


def enable_observability(containers: Containers) -> None:
    from deps_observability_instrumentation import (  # noqa: WPS433
        instrument_external_clients,
        instrument_messaging,
        setup_instrumentation,
    )

    logger.info("Instrumentation enabled.")

    setup_instrumentation()
    instrument_messaging(
        containers.messaging.producer(), containers.messaging.consumer()
    )
    instrument_external_clients(
        [
            containers.external_services.document_type_proxy(),
            containers.external_services.unifier_proxy(),
        ]
    )


def init_containers() -> Containers:
    settings = Settings()
    containers = Containers(
        messaging_driver_settings=settings.messaging_driver_settings
    )
    containers.config.from_pydantic(settings)
    containers.wire(
        (
            dispatcher,
            handlers,
        )
    )
    enable_auth(containers)

    if containers.config.instrumentation_enabled():
        enable_observability(containers)

    return containers
