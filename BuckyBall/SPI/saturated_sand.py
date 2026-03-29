# -*- coding: utf-8 -*-
"""
Concrete dataclass from SoilMat
Class for saturated sand

@author: Dr Alessandro Tombari
@author: Dr Giovanni Nicosia Li Destri
@fund: COWI Fonden 

---------

-------------
"""
from dataclasses import dataclass
import numpy as np
from adc_soilmat import SoilMat

@dataclass
class SaturatedSand(SoilMat):
    '''
    cu : float
        shear strength of the soil at depth z (represented by the residual shear strength Sr in the case of liquefied soil)
    e50 : float
        strain corresponding to one-half the maximum principal stress difference (0.05 for liquefied soil)
    J : float
        model factor typically equal to 0.5 for soft soils;
    '''
    cu: float | None = None
    e50: float | None = None
    J: float | None = None

    def updateProp(self) -> None:
        XYZ=self.XYZ
        if XYZ is not None:
            Z=XYZ[2]
        else:
            Z=0 # Default value if XYZ is not set
        if self.geff is not None:
            self.cu = self.geff*Z*0.05 #Boulanger 2007 
        else:
            raise ValueError("Effective unit weight must be defined to calculate shear strength.")
        pass
