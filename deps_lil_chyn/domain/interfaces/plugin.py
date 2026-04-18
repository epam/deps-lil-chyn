from abc import ABC, abstractmethod
from typing import Optional

from deps_unified_data import UnifiedData

from ..dto import UnifiedContainerData

__all__ = ["IUnifierPlugin"]


class IUnifierPlugin(ABC):
    document_type: Optional[str] = None

    @abstractmethod
    def unify(self, document_id: str, files: list[str]) -> UnifiedData:
        pass

    @abstractmethod
    def unify_container(self, document_id: int, file_path: str) -> UnifiedContainerData:
        pass
