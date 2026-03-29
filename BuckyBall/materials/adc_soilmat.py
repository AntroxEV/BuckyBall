# -*- coding: utf-8 -*-
"""
Abstract dataclass for soil material properties 

@author: Dr Alessandro Tombari


"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from BuckyBall.shared.abc_modelregistry import ModelRegistry


@dataclass
class SoilMat(ABC):
    """
    Abstract Class for Soil Material Properties.

    Parameters
    ----------
    phi : float
        friction angle of the soil [degrees]
    c : float
        cohesion of the soil [kPa]
    evoid : float
        soil void ratio [-]
    Gs : float
        specific gravity of soil solids [-]
    gwat : float
        unit weight of water [kN/m3]
    gsat : float
        saturated unit weight of the soil [kN/m3]
    geff : float
        average effective unit weight [kN/m3]
    _XYZ : tuple
        X-Y-Z coordinates of the soil element (optional, for spatially varying properties)

    """
    phi: float | None = None
    c: float | None = 0
    evoid: float | None = None
    Gs: float | None = None
    _gwat: float = 9.81
    gsat: float | None = None
    geff: float | None = None
    _XYZ: tuple | None = (0, 0, 0)

    @property
    def XYZ(self):
        return getattr(self, '_XYZ', None)
    @XYZ.setter
    def XYZ(self, value):
        if isinstance(value, tuple) and len(value) == 3:
            self._XYZ = value
        else:
            raise ValueError("XYZ must be a tuple of (X, Y, Z) coordinates.")
    
    def calc_gsat(self):
        if self.evoid is not None and self.Gs is not None:
            self.gsat = (self.evoid+self.Gs)*self._gwat/(1+self.evoid)
        else:
            raise ValueError("Void Ratio and Gs must be defined to calculate gsat.")
    def calc_geff(self):
        if self.gsat is not None:
            self.geff = self.gsat - self._gwat
        else:
            raise ValueError("Saturated unit weight must be defined to calculate effective unit weight.")
    def calc_dryweight(self):
        if self.gsat is not None and self.evoid is not None:
            return self.gsat*self._gwat/(1+self.evoid)
        else:
            raise ValueError("Saturated unit weight and void ratio must be defined to calculate dry weight.")
    
    def _set_ModelRegistry(self, model_name: str, registry: ModelRegistry) -> None: 
        """set the singleton instance of the model registry.

        """
        self._model_name = model_name
        self._registry = registry


    @abstractmethod
    def update_matprop(self) -> None:
        """
        Abstract method to update soil material properties through current position changes.
        
    
        """
        
        pass