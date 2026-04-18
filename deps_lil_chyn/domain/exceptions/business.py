from .base import BusinessException

__all__ = ["UnknownDocumentExtension", "MsgUnificationError", "DocUnificationError"]


class UnknownDocumentExtension(BusinessException):
    code = "unknown_document_extension"


class MsgUnificationError(BusinessException):
    code = "msg_unification_error"


class DocUnificationError(BusinessException):
    code = "doc_unification_error"
