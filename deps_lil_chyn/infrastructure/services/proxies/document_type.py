from http import HTTPStatus

from deps_lil_chyn.domain.exceptions import UnifierPluginAttachmentError
from deps_lil_chyn.domain.interfaces import IUnifierPlugin
from deps_lil_chyn.extras.rest_client import BaseRESTClient, DEPSApiKeyAuth
from deps_lil_chyn.infrastructure.access_management import user

from .deps_token_auth import DEPSTokenAuth

CommandChannel = str


__all__ = ["DocumentTypeProxy", "CommandChannel"]


class DocumentTypeProxy(BaseRESTClient):
    def _set_authentication(self) -> None:
        if self._api_key is not None:
            self._session.auth = DEPSApiKeyAuth(self._api_key)
        else:
            self._session.auth = DEPSTokenAuth(user)

    def attach_unifier_plugin(self, plugin: IUnifierPlugin) -> CommandChannel:
        attachment_url = f"{self._base_url}/plugins/attach-unifier"

        payload = {
            "document_type": plugin.document_type,
        }

        response = self._session.put(
            attachment_url,
            json=payload,
            timeout=60,
            verify=False,
        )

        if response.status_code != HTTPStatus.OK:
            raise UnifierPluginAttachmentError(response.content)

        return response.json()["command_channel"]
