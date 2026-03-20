# -*- coding: utf-8 -*-
"""
Abstract class for soil-pile-interaction curve models
They can be developed for p-y, q-z, t-z curves, and other types of curves related to soil-pile interaction.
Rotational M-R curves can also be implemented

@author: Dr Alessandro Tombari
---------
"""
from abc import ABC, abstractmethod
from adc_soilmat import SoilMat
from abc_pile import BasePile
from abc_modelregistry import ModelRegistry

class BaseSPICurve(ABC):
    def __init__(self, soil: SoilMat, pile: BasePile):
        self.data = soil
        self.pile = pile
        super().__init__()

    def update_soil(self, soil: SoilMat):
        self.data = soil
    
    def update_pile(self, pile: BasePile):
        self.pile = pile

    def get_soil(self) -> SoilMat:
        return self.data

    def get_pile(self) -> BasePile:
        return self.pile

    def update_loc(self,**kwargs) -> None:
        _X = kwargs.get('X', 0.0)          # default 0.0 if missing
        _Y = kwargs.get('Y', 0.0)
        _Z = kwargs.get('Z', 0.0)
        self.data.XYZ = (_X, _Y, _Z)
        self.data.update_matprop()

    def _set_ModelRegistry(self, model_name: str, registry: ModelRegistry) -> None: 
        """set the singleton instance of the model registry.

        """
        self._model_name = model_name
        self._registry = registry

    @abstractmethod
    def _build_FEM(self):
        '''Method to build the FEM model in the relevant software, to be implemented by concrete curve classes'''
        pass

