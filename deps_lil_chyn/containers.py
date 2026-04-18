from typing import Any, Optional, Type, Union

from dependency_injector import containers, providers, resources
from deps_asb import ASBClient, ASBConsumer, ASBProducer
from deps_kafka import KafkaClient, KafkaConsumer, KafkaProducer
from deps_message_flow import MessagingDriverEnum
from deps_message_flow.messaging.consumer import IMessageConsumer
from deps_message_flow.messaging.producer import IMessageProducer
from deps_object_storage import ObjectStorage, make_object_storage
from deps_rabbitmq import RabbitMQClient, RabbitMQConsumer, RabbitMQProducer

from deps_lil_chyn.application import Application
from deps_lil_chyn.domain.interfaces import IUnifierPlugin
from deps_lil_chyn.domain.services import VectorPdfExtractor
from deps_lil_chyn.infrastructure.services import (
    CsvUnifier,
    DocumentTypeProxy,
    DocUnifier,
    DocxUnifier,
    EmlUnifier,
    ExcelUnifier,
    ImageUnifier,
    MsgUnifier,
    PdfUnifier,
    TiffUnifier,
    UnifierProxy,
)

MessagingClient = Union[ASBClient, KafkaClient, RabbitMQClient]


class MessageBrokerResource(resources.Resource):
    def init(  # type: ignore
        self,
        driver_type: str,
        expected_driver: str,
        client: Type[MessagingClient],
        message_connection_string: str,
        **kwargs: dict[str, Any],
    ) -> Optional[MessagingClient]:
        return (
            client(message_connection_string, **kwargs)
            if driver_type == expected_driver
            else None
        )

    def shutdown(self, resource: Optional[MessagingClient]) -> None:  # type: ignore
        if resource:
            resource.close()


class MessageBrokers(containers.DeclarativeContainer):
    config = providers.Configuration()
    messaging_driver_settings = providers.Dependency(instance_of=object)

    broker_client: providers.Provider[MessagingClient] = providers.Selector(
        config.messaging_driver,
        asb=providers.Resource(
            MessageBrokerResource,
            driver_type=MessagingDriverEnum.ASB.value,
            expected_driver=config.messaging_driver,
            client=ASBClient,
            message_connection_string=config.message_broker_connection_string,
            asb_settings=messaging_driver_settings,
        ),
        kafka=providers.Resource(
            MessageBrokerResource,
            driver_type=MessagingDriverEnum.KAFKA.value,
            expected_driver=config.messaging_driver,
            client=KafkaClient,
            message_connection_string=config.message_broker_connection_string,
            settings=messaging_driver_settings,
        ),
        rabbitmq=providers.Resource(
            MessageBrokerResource,
            driver_type=MessagingDriverEnum.RABBITMQ.value,
            expected_driver=config.messaging_driver,
            client=RabbitMQClient,
            message_connection_string=config.message_broker_connection_string,
            settings=messaging_driver_settings,
        ),
    )


class Messaging(containers.DeclarativeContainer):
    config = providers.Configuration()
    message_brokers = providers.DependenciesContainer()

    producer: providers.Provider[IMessageProducer] = providers.Selector(
        config.messaging_driver,
        asb=providers.Singleton(
            ASBProducer,
            client=message_brokers.broker_client,
            topic_name=config.messaging_driver_settings.topic_name,
        ),
        kafka=providers.Singleton(
            KafkaProducer,
            client=message_brokers.broker_client,
        ),
        rabbitmq=providers.Singleton(
            RabbitMQProducer,
            client=message_brokers.broker_client,
        ),
    )
    consumer: providers.Provider[IMessageConsumer] = providers.Selector(
        config.messaging_driver,
        asb=providers.Singleton(
            ASBConsumer,
            client=message_brokers.broker_client,
            topic_name=config.messaging_driver_settings.topic_name,
            custom_subscription_name=config.messaging_driver_settings.subscription_name,
        ),
        kafka=providers.Singleton(
            KafkaConsumer,
            client=message_brokers.broker_client,
        ),
        rabbitmq=providers.Singleton(
            RabbitMQConsumer,
            client=message_brokers.broker_client,
        ),
    )


class ExternalServices(containers.DeclarativeContainer):
    config = providers.Configuration()

    object_storage: providers.Provider[ObjectStorage] = providers.Singleton(
        make_object_storage
    )

    document_type_proxy: providers.Provider[DocumentTypeProxy] = providers.Singleton(
        DocumentTypeProxy,
        base_url=config.document_type_url,
        api_key=config.api_key,
    )
    unifier_proxy: providers.Provider[UnifierProxy] = providers.Singleton(
        UnifierProxy,
        base_url=config.unifier_url,
        api_key=config.api_key,
    )


class DomainServices(containers.DeclarativeContainer):
    vector_pdf_extractor: providers.Provider[VectorPdfExtractor] = providers.Singleton(
        VectorPdfExtractor
    )


class Unifiers(containers.DeclarativeContainer):
    config = providers.Configuration()

    object_storage: providers.Provider[ObjectStorage] = providers.Dependency()
    vector_pdf_extractor: providers.Provider[
        VectorPdfExtractor
    ] = providers.Dependency()
    unifier_proxy: providers.Provider[UnifierProxy] = providers.Dependency()

    pdf: providers.Provider[PdfUnifier] = providers.Singleton(
        PdfUnifier,
        object_storage=object_storage,
        vector_pdf_extractor=vector_pdf_extractor,
        target_dpi=config.target_dpi,
        max_processes=config.pdf_max_processes,
    )
    image: providers.Provider[ImageUnifier] = providers.Singleton(
        ImageUnifier,
        object_storage=object_storage,
    )
    tiff: providers.Provider[TiffUnifier] = providers.Singleton(
        TiffUnifier,
        object_storage=object_storage,
    )
    excel: providers.Provider[ExcelUnifier] = providers.Singleton(
        ExcelUnifier,
        object_storage=object_storage,
        unifier_proxy=unifier_proxy,
        cell_chunk_size=config.cell_chunk_size,
    )
    doc: providers.Provider[DocUnifier] = providers.Singleton(
        DocUnifier,
        object_storage=object_storage,
        unifier_proxy=unifier_proxy,
    )
    docx: providers.Provider[DocxUnifier] = providers.Singleton(
        DocxUnifier,
        object_storage=object_storage,
        unifier_proxy=unifier_proxy,
    )
    eml: providers.Provider[EmlUnifier] = providers.Singleton(
        EmlUnifier,
        object_storage=object_storage,
        supported_attachment_extensions=config.supported_attachment_extensions,
    )
    msg: providers.Provider[MsgUnifier] = providers.Singleton(
        MsgUnifier,
        object_storage=object_storage,
        converter_script_path=config.msg_to_eml_converter_script_path,
        supported_attachment_extensions=config.supported_attachment_extensions,
    )
    csv: providers.Provider[CsvUnifier] = providers.Singleton(
        CsvUnifier,
        object_storage=object_storage,
        unifier_proxy=unifier_proxy,
        cell_chunk_size=config.cell_chunk_size,
    )


class Containers(containers.DeclarativeContainer):
    config = providers.Configuration()
    messaging_driver_settings = providers.Dependency(instance_of=object)
    external_services: providers.Container[ExternalServices] = providers.Container(
        ExternalServices, config=config
    )

    message_brokers: providers.Container[MessageBrokers] = providers.Container(
        MessageBrokers,
        config=config,
        messaging_driver_settings=messaging_driver_settings,
    )

    messaging: providers.Container[Messaging] = providers.Container(
        Messaging, config=config, message_brokers=message_brokers
    )

    domain_services: providers.Container[DomainServices] = providers.Container(
        DomainServices
    )

    unifiers: providers.Container[Unifiers] = providers.Container(
        Unifiers,
        config=config,
        object_storage=external_services.object_storage,
        vector_pdf_extractor=domain_services.vector_pdf_extractor,
        unifier_proxy=external_services.unifier_proxy,
    )

    plugin: providers.Provider[IUnifierPlugin] = providers.Dependency()

    application: providers.Singleton[Application] = providers.Singleton(
        Application,
        document_type_proxy=external_services.document_type_proxy,
        default_command_channel=config.default_command_channel,
        plugin=plugin,
    )
