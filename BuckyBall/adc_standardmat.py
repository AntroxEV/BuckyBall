# -*- coding: utf-8 -*-
"""
Abstract dataclass for standard uniaxial materials

@author: Dr Alessandro Tombari


---------
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from abc_modelregistry import ModelRegistry

@dataclass
class UniaxialMaterial(ABC):
    """
    Abstract dataclass for standard uniaxial materials.
    """

    # --- Material parameters (immutable after construction) ---
    Einit: float
    rho: float = 0.0
    nu: float | None = None
    _Ginit: float | None = None


    # --- State variables (mutable, not part of dataclass identity) ---
    _XYZ: tuple = field(default_factory=lambda: (0, 0, 0), init=False, repr=False)
    _Etang: float = field(default=1.0, init=False, repr=False)

    # --- Properties for controlled access ---
    @property
    def Etang(self):
        return self._Etang

    @Etang.setter
    def Etang(self, value):
        if value <= 0:
            raise ValueError("Etang must be positive.")
        self._Etang = value

    @property
    def XYZ(self):
        return self._XYZ

    @XYZ.setter
    def XYZ(self, value):
        if isinstance(value, tuple) and len(value) == 3:
            self._XYZ = value
        else:
            raise ValueError("XYZ must be a tuple of (X, Y, Z).")
    
    def _set_ModelRegistry(self, model_name: str, registry: ModelRegistry) -> None: 
        """set the singleton instance of the model registry.

        """
        self._model_name = model_name
        self._registry = registry


    # --- Validation ---
    def __post_init__(self):
        if self.Einit <= 0:
            raise ValueError("Initial elastic modulus Einit must be positive.")

        if self.rho is not None and self.rho < 0:
            raise ValueError("Density rho cannot be negative.")
        
        if self.rho is None:
            self.rho = 0.0

        if self.nu is not None:
            if not (0 <= self.nu < 0.5):
                raise ValueError("Poisson's ratio must be between 0 and 0.5.")
            
        self._Ginit = self.Einit / (2 * (1 + self.nu)) if self.nu is not None else None
    
    

    # --- Abstract methods ---
    @abstractmethod
    def get_stress(self, strain: float) -> float:
        ...

    @abstractmethod
    def get_tangent_modulus(self, strain: float) -> float:
        ...
    
    @abstractmethod
    def updateProp(self) -> None:
        ...
    
    
