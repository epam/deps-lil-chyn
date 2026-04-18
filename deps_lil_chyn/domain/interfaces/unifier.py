from typing import List, Protocol

from deps_unified_data.model import UnifiedData

__all__ = ["Unifier"]


class Unifier(Protocol):
    def unify(self, document_id: int, files: List[str]) -> UnifiedData:
        pass
