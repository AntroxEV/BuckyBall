# -*- coding: utf-8 -*-
"""
Abstract dataclass for cross-sectional properties

@author: Dr Alessandro Tombari
@author: Dr Giovanni Nicosia Li Destri
@funder: COWI Fonden 

---------
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class CrossSection(ABC):

    @property
    @abstractmethod
    def Ix(self) -> float:
        """Moment of inertia about the x-axis [m^4]
        """
        pass
    @property
    @abstractmethod
    def Iy(self) -> float:
        """Moment of inertia about the y-axis [m^4]
        """
        pass
    @property
    @abstractmethod
    def Jxy(self) -> float:
        """Torsional constant [m^4]
        """
        pass
    @property
    @abstractmethod
    def As(self) -> float:
        """Shear area [m^2]
        """
        pass
    @property
    @abstractmethod
    def A(self) -> float:
        """Cross-sectional area [m^2]
        """
        pass
    @property
    @abstractmethod
    def equivbreadth(self) -> float:
        """equivalent breadth or width of the section [m]
        """
        pass
