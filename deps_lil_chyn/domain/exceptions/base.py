__all__ = [
    "BaseUnifierPluginException",
    "UnifierPluginAttachmentError",
    "SaveUnifiedDataError",
    "BusinessException",
]


class BaseUnifierPluginException(Exception):
    code = "unifier_plugin_exception"


class BusinessException(BaseUnifierPluginException):
    code = "business_exception"


class UnifierPluginAttachmentError(BaseUnifierPluginException):
    code = "unifier_plugin_attachment_error"


class SaveUnifiedDataError(BaseUnifierPluginException):
    code = "save_unified_data_error"
