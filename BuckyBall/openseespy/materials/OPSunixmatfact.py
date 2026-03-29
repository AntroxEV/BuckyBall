# -*- coding: utf-8 -*-
"""
   Factory and registry for OpenSeesPy uniaxial material classes.

    This class maintains a class-level registry that maps material names
    to their corresponding Python classes. Material classes register
    themselves using the `@OpsUnixMatFactory.register(name)` decorator,
    which inserts the class into the registry at import time.

    The `create(name, *args, **kwargs)` method acts as a factory:
    it looks up the material class associated with the given name and
    returns an instantiated object using the provided arguments.

    This pattern avoids large conditional or match-case dispatch blocks
    and supports extensibility, allowing new material types to be added
    simply by defining a class and decorating it with `@register`.

@author: Dr Alessandro Tombari

"""
from __future__ import annotations

class OpsUnixMatFactory:
    _registry = {}

    @classmethod
    def register(cls, name):
        def decorator(material_cls):
            cls._registry[name] = material_cls
            return material_cls
        return decorator

    @classmethod
    def create(cls, name, *args, **kwargs):
        if name not in cls._registry:
            raise ValueError(f"Unknown material: {name}")
        return cls._registry[name](*args, **kwargs)