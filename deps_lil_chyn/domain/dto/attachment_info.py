from dataclasses import dataclass

__all__ = ["AttachmentInfo"]


@dataclass
class AttachmentInfo:
    title: str
    blob_name: str
