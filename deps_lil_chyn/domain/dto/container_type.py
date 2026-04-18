from enum import Enum

__all__ = ["ContainerType"]


class ContainerType(str, Enum):
    EMAIL = "email"
