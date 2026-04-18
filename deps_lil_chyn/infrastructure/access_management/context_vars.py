import contextvars

from deps_lil_chyn.extras.value_objects import UserValueObject

__all__ = ["user"]


user: contextvars.ContextVar[UserValueObject] = contextvars.ContextVar("user")
