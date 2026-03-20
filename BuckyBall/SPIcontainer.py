# -*- coding: utf-8 -*-
"""
Container/Registry Class for soil-pile interaction curves.
It is a typed dependency container class (store validate expose) 
@author: Dr Alessandro Tombari

"""
from abc_pycurve import BasePYCurve
from abc_qzcurve import BaseQZCurve
from abc_tzcurve import BaseTZCurve
from abc_spicurve import BaseSPICurve

class SPI:
    ROLE_SPECS = {
        "py_x": BasePYCurve,
        "py_y": BasePYCurve,
        "qz":   BaseQZCurve,
        "tz":   BaseTZCurve,
    }

    def __init__(self, *, py_x=None, py_y=None, qz=None, tz=None):
        provided = {"py_x": py_x, "py_y": py_y, "qz": qz, "tz": tz}

        for role, instance in provided.items():
            self._validate_instance(role, instance, self.ROLE_SPECS[role])

        # Store instances directly in fixed order
        self._items = [py_x, py_y, qz, tz]

    def _validate_instance(self, name, instance, expected):
        if instance is None:
            return
        if not isinstance(instance, expected):
            raise TypeError(
                f"Role '{name}' expects an instance of {expected.__name__}, "
                f"got {type(instance).__name__}"
            )

    def _set(self, position, instance: BaseSPICurve | None):
        expected_cls = list(self.ROLE_SPECS.values())[position]

        if instance is None:
            self._items[position] = None
            return

        if not isinstance(instance, expected_cls):
            raise TypeError(
                f"Position {position} expects {expected_cls.__name__}, "
                f"got {type(instance).__name__}"
            )

        self._items[position] = instance

 
    def set_py_x(self, item : BasePYCurve | None): self._set(0, item)
    def set_py_y(self, item : BasePYCurve | None): self._set(1, item)
    def set_qz(self, item: BaseQZCurve | None):   self._set(2, item)
    def set_tz(self, item: BaseTZCurve | None):   self._set(3, item)

    def get_py_x(self) -> BasePYCurve | None: return self._get(0)
    def get_py_y(self)-> BasePYCurve | None: return self._get(1)
    def get_qz(self)-> BaseQZCurve | None:   return self._get(2)
    def get_tz(self)-> BaseTZCurve | None:   return self._get(3)


    def _get(self, position):
        return self._items[position]
