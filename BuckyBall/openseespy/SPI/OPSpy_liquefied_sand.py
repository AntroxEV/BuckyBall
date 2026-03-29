# -*- coding: utf-8 -*-
"""
Concrete Classes for py curves

@author: Dr Alessandro Tombari


---------
"""
from ops_abc_pycurve import OpsBasePYCurve
import numpy as np
from BuckyBall.SPI.saturated_sand import SaturatedSand
from BuckyBall.elements.abc_pile import BasePile


# Existing p-y Models for Liquefied Soil
class py_WangReese1998(OpsBasePYCurve):
    def __init__(self, soil: SaturatedSand, pile: BasePile):
        super().__init__(soil, pile)

    def calc_py(self, dp: float, y: float, z: float) -> float: 
        self.update_loc(Z=z)
        pu1 = (3+self.data.geff/self.data.cu*z+self.data.J/dp*z)*self.data.cu*dp #unsafe 
        pu2 = 9*self.data.cu*dp
        pu = np.min([pu1,pu2])
        p = 0.5*pu*(y/(2.5*self.data.e50*dp))**(1/3)
        return p
    
class  py_Rollins2005(OpsBasePYCurve):
    def __init__(self, soil: SaturatedSand, pile: BasePile):
        super().__init__(soil, pile)
    
    def calc_py(self, dp: float, y: float, z: float) -> float: 
        print("Rollins 2005 curve - input values must be provided in m")
        print("units are unchecked - user must ensure correct units are used")
        y=y*1000 #transform m to mm
        A = 3e-7 * (z+1)**6.05
        B = 2.8*(z+1)**0.11
        C = 2.85*(z+1)**(-0.41)
        pd= 3.81*np.log(dp) + 5.6
        return A*(B*y)**C*pd
    

class py_Frankehybr(OpsBasePYCurve):
    def __init__(self, soil: SaturatedSand, pile: BasePile):
        self.curve1 = py_Rollins2005(soil, pile)
        self.curve2 = py_WangReese1998(soil, pile)
    def calc_py(self, dp: float, y: float, z: float) -> float: 
        p1=self.curve1.calc_py(dp, y, z)
        p2=self.curve2.calc_py(dp, y, z)
        return np.min([p1,p2])