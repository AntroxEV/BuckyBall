# -*- coding: utf-8 -*-
"""
Concrete Classes for py curves

@author: Dr Alessandro Tombari


---------
"""
from abc_pycurve import BasePYCurve
import numpy as np
from saturated_sand import SaturatedSand
from abc_pile import BasePile

# Existing p-y Models for Liquefied Soil
class py_WangReese1998(BasePYCurve):
    def __init__(self, soil: SaturatedSand, pile: BasePile):
        super().__init__(soil, pile)

        
        
    def calc_py(self, dp: float, y: float, z: float) -> float: 
        self.update_loc(Z=z)
        pu1 = (3+self.data.geff/self.data.cu*z+self.data.J/dp*z)*self.data.cu*dp #unsafe 
        pu2 = 9*self.data.cu*dp
        pu = np.min([pu1,pu2])
        p = 0.5*pu*(y/(2.5*self.data.e50*dp))**(1/3)
        return p
    
class py_Rollins2005(BasePYCurve):
    def __init__(self, soil: SaturatedSand, pile: BasePile):
        super().__init__(soil, pile)
    
    def calc_py(self, dp: float, y: float, z: float) -> float: 
        y=y*1000 #transform m to mm
        A = 3e-7 * (z+1)**6.05
        B = 2.8*(z+1)**0.11
        C = 2.85*(z+1)**(-0.41)
        pd= 3.81*np.log(dp) + 5.6
        return A*(B*y)**C*pd

class py_Frankehybr(BasePYCurve):
    def __init__(self, soil: SaturatedSand, pile: BasePile):
        self.curve1 = py_Rollins2005(soil, pile)
        self.curve2 = py_WangReese1998(soil, pile)
    def calc_py(self, dp: float, y: float, z: float) -> float: 
        p1=self.curve1.calc_py(dp, y, z)
        p2=self.curve2.calc_py(dp, y, z)
        return np.min([p1,p2])