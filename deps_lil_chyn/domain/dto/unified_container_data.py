from dataclasses import dataclass

from .attachment_info import AttachmentInfo
from .container_metadata import ContainerMetadata
from .container_type import ContainerType

__all__ = ["UnifiedContainerData"]


@dataclass
class UnifiedContainerData:
    container_type: ContainerType
    container_metadata: ContainerMetadata
    attachments: list[AttachmentInfo]
