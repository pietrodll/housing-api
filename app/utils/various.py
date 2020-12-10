"""This module contains various utilities"""

from typing import Any
from flask import g

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwds)

        return cls._instances[cls]


class FlaskSingletonMeta(type):
    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        name = cls.FLASK_G_ID

        if name not in g:
            setattr(g, name, super().__call__(*args, **kwds))
        
        return getattr(g, name)
