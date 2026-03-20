# -*- coding: utf-8 -*-
"""
Concrete dataclass for elastic uniaxial materials

@author: Dr Alessandro Tombari
@author: Dr Giovanni Nicosia Li Destri
@funder: COWI Fonden 

---------
"""
from dataclasses import dataclass
from adc_standardmat import UniaxialMaterial

@dataclass
class PerfectlyPlasticMat(UniaxialMaterial):
    """
    Perfectly plastic uniaxial material.
    """

    fy: float = 0.0  # yield stress

    def __post_init__(self):
        super().__post_init__()

        if self.fy < 0:
            raise ValueError("Yield stress fy must be non-negative.")

    # --- Stress computation ---
    def get_stress(self, strain: float) -> float:
        eps_y = self.fy / self.Einit

        if abs(strain) <= eps_y:
            return strain * self.Einit
        else:
            return self.fy if strain >= 0 else -self.fy

    # --- Tangent modulus ---
    def get_tangent_modulus(self, strain: float) -> float:
        eps_y = self.fy / self.Einit

        if abs(strain) <= eps_y:
            self.Etang = self.Einit
        else:
            self.Etang = 0.0

        return self.Etang