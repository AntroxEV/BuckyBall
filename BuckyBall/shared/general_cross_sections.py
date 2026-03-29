# -*- coding: utf-8 -*-
"""
Classes for typical cross-sections

@author: Dr Alessandro Tombari
@author: Dr Giovanni Nicosia Li Destri
@funder: COWI Fonden 

---------
"""
from adc_cross_section import CrossSection
import numpy as np
from dataclasses import dataclass

@dataclass
class Rectangle(CrossSection):
    _width: float = 1
    _height: float= 1


    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = value

    @property
    def Ix(self):
        return (self.width * self.height**3) / 12   
    @property
    def Iy(self):               
        return (self.height * self.width**3) / 12
    @property
    def Jxy(self):
        return self.Ix + self.Iy
    @property
    def As(self):
        return self.width * self.height 
    @property
    def A(self):
        return self.width * self.height 
    @property
    def equivbreadth(self):
        return self.width
    

@dataclass
class Circle(CrossSection):
    _diameter: float = 1

    @property
    def Dc(self):
        return self._diameter

    @Dc.setter
    def Dc(self, value):
        if value <= 0:
            raise ValueError("Diameter must be positive")
        self._diameter = value

    @property
    def Ix(self):
        return (np.pi * self.Dc**4) / 64   
    @property
    def Iy(self):               
        return (np.pi * self.Dc**4) / 64
    @property
    def Jxy(self):
        return (np.pi * self.Dc**4) / 32
    @property
    def As(self):
        return (np.pi * self.Dc**2) / 4 
    @property
    def A(self):
        return (np.pi * self.Dc**2) / 4
    @property
    def equivbreadth(self):
        return self.Dc
    
@dataclass
class HollowCircle(CrossSection):
    """
    Hollow circular cross-section defined by outer diameter, inner diameter, and thickness.
    At least two of the three parameters must be provided to compute the third. 
    
    Parameters
    ----------
     Dout: float
        Outer diameter of the hollow circle [m]
     Din: float
        Inner diameter of the hollow circle [m]
    th: float
        Thickness of the hollow circle wall [m]
            
    """
    Dout: float | None = None
    Din: float | None = None
    th: float | None = None

    def __post_init__(self):
        # Count how many values were provided
        provided = sum(v is not None for v in (
            self.Dout, self.Din, self.th
        ))

        if provided < 2:
            raise ValueError("At least two of Dout, Din, th must be provided")

        # Compute missing value
        if self.Dout is None:
            self.Dout = self.Din + 2 * self.th  

        elif self.Din is None:
            self.Din = self.Dout - 2 * self.th

        elif self.th is None:
            self.th = (self.Dout - self.Din) / 2

        # Validate geometry
        if self.Dout <= 0:
            raise ValueError("Outer diameter must be positive")
        if self.Din < 0:
            raise ValueError("Inner diameter cannot be negative")
        if self.Din >= self.Dout:
            raise ValueError("Inner diameter must be smaller than outer diameter")
        if self.th <= 0:
            raise ValueError("Thickness must be positive")


    @property
    def Ix(self):
        return (np.pi * (self.Dout**4 - self.Din**4)) / 64   
    @property
    def Iy(self):               
        return (np.pi * (self.Dout**4 - self.Din**4)) / 64
    @property
    def Jxy(self):
        return (np.pi * (self.Dout**4 - self.Din**4)) / 32
    @property
    def As(self):
        return (self.Dout**2 - self.Din**2) / 2 
    @property
    def A(self):
        return (np.pi * (self.Dout**2 - self.Din**2)) / 4
    @property
    def equivbreadth(self):
        return self.Dout

                                        