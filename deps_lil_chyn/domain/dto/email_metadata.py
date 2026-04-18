from dataclasses import dataclass
from typing import Optional

from .container_metadata import ContainerMetadata

__all__ = ["EmailMetadata"]


@dataclass
class EmailMetadata(ContainerMetadata):
    recipients: list[str]
    cc: list[str]
    subject: Optional[str] = None
    sender: Optional[str] = None
    body: Optional[str] = None
    date: Optional[str] = None
