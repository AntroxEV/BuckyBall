# -*- coding: utf-8 -*-
"""
Abstract Class for Embedded Piles.
It is a generic wrapper class to add soil-pile interaction elements to the pile elements.

@author: Dr Alessandro Tombari

"""
from abc import ABC, abstractmethod
from BuckyBall.elements.abc_pile import BasePile
from SPIcontainer import SPI

class BaseEmbedded(ABC):
        allowed_pile = BasePile
        allowed_spi = SPI
    

        def __init__(self, cpile, cspi):
            if not isinstance(cpile, self.allowed_pile):
                raise TypeError("BasePile instance expected as first argument.")
            if not isinstance(cspi, self.allowed_spi):
                raise TypeError("SPI instance expected as second argument.")

            self._cpile = cpile
            self._cspi = cspi

        # delegation logic to allow access to BasePile and SPI attributes and methods
        # cpile is primary and cspi is secondary for delegation (fallback subsystem)
        # - If not found, __getattr__ runs if method is not defined in the wrapper 
        # (otherswise it would call the wrapper method) 
        def __getattr__(self, name):
            if hasattr(self._cpile, name):
                return getattr(self._cpile, name)
            if hasattr(self._cspi, name):
                return getattr(self._cspi, name)
            raise AttributeError(name)


        @abstractmethod
        def _add_soil_pile_interaction(self):
            pass

        @abstractmethod
        def _build_FEM(self):
            pass





