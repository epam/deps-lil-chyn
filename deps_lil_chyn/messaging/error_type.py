import enum

__all__ = ["ErrorType"]


class ErrorType(str, enum.Enum):
    SYSTEM = "system"
    BUSINESS = "business"
