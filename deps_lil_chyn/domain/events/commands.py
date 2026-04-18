from dataclasses import dataclass
from typing import Any, Optional

from deps_message_flow.commands.common import Command

__all__ = [
    "UnifyDocument",
    "PerformUnificationReply",
    "UnifyContainerDocument",
    "PerformContainerUnificationReply",
]


@dataclass
class UnifyDocument(Command):
    document_id: str
    files: list[str]


@dataclass
class PerformUnificationReply(Command):
    error_type: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class UnifyContainerDocument(Command):
    document_id: int
    file_path: str


@dataclass
class PerformContainerUnificationReply(Command):
    container_type: Optional[str] = None
    container_metadata: Optional[dict[str, Any]] = None
    attachments: Optional[list[dict[str, Any]]] = None
    error_type: Optional[str] = None
    error_message: Optional[str] = None
