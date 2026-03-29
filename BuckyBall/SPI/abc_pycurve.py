# -*- coding: utf-8 -*-
"""
Abstract class for p-y curve models

@author: Dr Alessandro Tombari
---------
"""
from abc import ABC, abstractmethod
from adc_soilmat import SoilMat
from abc_pile import BasePile
from abc_spicurve import BaseSPICurve

class BasePYCurve(BaseSPICurve):
    def __init__(self, soil: SoilMat, pile: BasePile):
        super().__init__(soil, pile)

    
    @abstractmethod
    def calc_py(self, dp: float, y: float, z: float) -> float:
        """
        Parameters
        ----------
        data : SoilMat
            define SoilMat class
        dp: float
                Pile diameter [m]
        z : float
            Depth below ground surface. [m]
        y : float
            Pile Lateral displacement [m]
            
        Returns
        -------
        float
            Computed soil resistance per unit length of pile [kN/m]
        """
        pass

