import logging

from deps_lil_chyn.domain.dto import UnifiedContainerData
from deps_lil_chyn.domain.interfaces import IUnifierPlugin
from deps_lil_chyn.infrastructure.services import CommandChannel, DocumentTypeProxy

__all__ = ["Application"]


class Application:
    def __init__(
        self,
        document_type_proxy: DocumentTypeProxy,
        default_command_channel: CommandChannel,
        plugin: IUnifierPlugin,
    ):
        self._document_type_proxy = document_type_proxy
        self._default_command_channel = default_command_channel
        self._plugin = plugin

        self._logger = logging.getLogger(self.__class__.__name__)

    def get_command_channel(self, plugin: IUnifierPlugin) -> CommandChannel:
        if doc_type := plugin.document_type:
            self._logger.info(f"Registering plugin with type {doc_type}...")
            command_channel = self.attach_plugin(plugin)

        else:
            command_channel = (
                self._default_command_channel
            )  # For generic plugins registration

        return command_channel

    def attach_plugin(self, plugin: IUnifierPlugin) -> CommandChannel:
        return self._document_type_proxy.attach_unifier_plugin(plugin=plugin)

    def unify_document(self, document_id: str, files: list[str]) -> None:
        self._plugin.unify(document_id, files)

    def unify_container_document(
        self, document_id: int, file_path: str
    ) -> UnifiedContainerData:
        return self._plugin.unify_container(
            document_id=document_id, file_path=file_path
        )
