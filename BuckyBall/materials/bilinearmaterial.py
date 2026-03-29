# -*- coding: utf-8 -*-
"""
Concrete dataclass for bilinear uniaxial materials

@author: Dr Alessandro Tombari
@author: Dr Giovanni Nicosia Li Destri
@funder: COWI Fonden 

---------
"""
from dataclasses import dataclass
from adc_standardmat import UniaxialMaterial

@dataclass
class BilinearMat(UniaxialMaterial):
    """
    Bilinear uniaxial material with elastic-plastic behavior.
    """

    fy: float = 0.0                 # yield stress (positive)
    Eplastic: float | None = None  # tangent modulus after yielding

    def __post_init__(self):
        super().__post_init__()

        if self.fy < 0:
            raise ValueError("Yield stress fy must be non-negative.")

        if self.Eplastic is None:
            raise ValueError("Eplastic must be provided for a bilinear material.")

        if self.Eplastic < 0:
            raise ValueError("Eplastic must be non-negative.")

    # --- Stress computation ---
    def get_stress(self, strain: float) -> float:
        eps_y = self.fy / self.Einit

        if abs(strain) <= eps_y:
            # Elastic region
            return strain * self.Einit
        else:
            # Plastic region (bilinear)
            sign = 1 if strain >= 0 else -1
            plastic_strain = abs(strain) - eps_y
            return sign * (self.fy + plastic_strain * self.Eplastic)

    # --- Tangent modulus ---
    def get_tangent_modulus(self, strain: float) -> float:
        eps_y = self.fy / self.Einit

        if abs(strain) <= eps_y:
            self.Etang = self.Einit
        else:
            self.Etang = self.Eplastic

        return self.Etang
    
    def updateProp(self, XYZ: tuple) -> None:
        # For a bilinear material, properties do not change with XYZ, so this is a no-op.
        pass
    