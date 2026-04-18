from http import HTTPStatus

from deps_unified_data import Cell, UnifiedData
from deps_unified_data.serializers import SerializedCell, SerializedUnifiedData

from deps_lil_chyn.domain.exceptions import SaveUnifiedDataError
from deps_lil_chyn.extras.rest_client import BaseRESTClient, DEPSApiKeyAuth
from deps_lil_chyn.infrastructure.access_management import user

from .deps_token_auth import DEPSTokenAuth

__all__ = ["UnifierProxy"]


class UnifierProxy(BaseRESTClient):
    def _set_authentication(self) -> None:
        if self._api_key is not None:
            self._session.auth = DEPSApiKeyAuth(self._api_key)
        else:
            self._session.auth = DEPSTokenAuth(user)

    def save_unified_data(self, unified_data: UnifiedData) -> None:
        url = f"{self._base_url}/unified_data/upsert-data"

        payload = SerializedUnifiedData.from_model(unified_data).dict(by_alias=True)

        response = self._session.put(
            url,
            json=payload,
            timeout=60,
            verify=False,
        )

        if response.status_code != HTTPStatus.OK:
            raise SaveUnifiedDataError(response.content)

    def save_cells(self, cells: list[Cell]) -> None:
        url = f"{self._base_url}/cells"

        payload = [
            SerializedCell.from_model(cell).dict(by_alias=True) for cell in cells
        ]

        response = self._session.post(
            url,
            json=payload,
            timeout=60,
            verify=False,
        )

        if response.status_code != HTTPStatus.CREATED:
            raise SaveUnifiedDataError(response.content)
