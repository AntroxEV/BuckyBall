# -*- coding: utf-8 -*-
"""
Concrete dataclass for elastic uniaxial materials

@author: Dr Alessandro Tombari
@author: Dr Giovanni Nicosia Li Destri
@funder: COWI Fonden 

---------
"""

from abc import abstractmethod
from dataclasses import dataclass
from adc_standardmat import UniaxialMaterial

from dataclasses import dataclass

@dataclass
class ElasticMat(UniaxialMaterial):
    """
    Dataclass for elastic uniaxial materials.
    """

    Eneg: float | None = None  # tangent modulus in compression

    def __post_init__(self):
        # Run base validation first
        super().__post_init__()

        # Validate or set Eneg
        if self.Eneg is None:
            self.Eneg = self.Einit
        else:
            if self.Eneg <= 0:
                raise ValueError("Eneg must be positive.")

    def get_stress(self, strain: float) -> float:
        if strain < 0:
            return strain * self.Eneg
        else:
            return strain * self.Einit

    def get_tangent_modulus(self, strain: float) -> float:
        return self.Eneg if strain < 0 else self.Einit
    
    def update_property(self, XYZ: tuple) -> None:
        # For an elastic material, properties do not change with XYZ, so this is a no-op.
        pass
    
    
