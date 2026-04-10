# -*- coding: utf-8 -*-
"""
    Abstract Class for Composite Pile Properties and Methods.
    It is a generic wrapper class to combine multiple pile elements (e.g., a pile and an embedded pile) into a single composite pile element.
    It is usefdul for modelling composite piles (e.g., pile groups, pile with embedded portion) where the pile elements are connected in series 
    It can be used to model layered piles (e.g., pile with different materials or cross-sections along its length) by combining multiple pile elements with different properties.
    Each embedded pile can have its own soil-pile interaction properties, allowing for more accurate modelling of the pile-soil interaction along the length of the pile.
    

@author: Dr Alessandro Tombari

-------------
"""
from abc import ABC, abstractmethod
from BuckyBall.elements.abc_pile import BasePile
from BuckyBall.SPI.abc_embedded import BaseEmbedded
from typing import TypeVar, Generic, Union, List
from BuckyBall.shared.builderregistry import ModelBuilderRegistry

Pile=TypeVar('Pile', bound=BasePile)
Embedded=TypeVar('Embedded', bound=BaseEmbedded)
PileType=Union[Pile, Embedded]


class BaseCompositePile(ABC, Generic[Pile,Embedded]): 
    
    app_name: str #must be defined in subclass to specify the third-party application to wrap (e.g., "OpenSees", "Plaxis", etc.)

    def __init__(self, segments: List[PileType]):
        if not all(isinstance(seg, (BasePile, BaseEmbedded)) for seg in segments):
            raise TypeError("All segments must be instances of BasePile or BaseEmbedded.")
        self._segments = segments
        #self-registration in the ModelBuilderRegistry:
        ModelBuilderRegistry._register(self.app_name, self.__class__, self)  # Register the instance in the ModelBuilderRegistry


    def __add__(self, other):
        if isinstance(other, BaseCompositePile):
            return self._combine_with(self._segments + other._segments)
        elif isinstance(other, (BasePile, BaseEmbedded)):
            return self._combine_with(self._segments + [other]) 
        return NotImplemented
    
    def __post_init__(self):
        Zbotm = []
        for seg in self._segments:
            if isinstance(seg, BaseEmbedded):
                Zbotm.append(seg._cpile._edges[1])  # interface depth
            elif isinstance(seg, BasePile):
                    Zbotm.append(seg._edges[1])  # pile tip depth
            else:
                raise TypeError("Segment must be either BasePile or BaseEmbedded.")
            if len(Zbotm) >1:
                if Zbotm[-1] != Zbotm[-2]:
                    raise ValueError("Segments must be connected in series (matching depths).")

    @abstractmethod
    def _combine_with(self, new_segments: List[PileType]) -> 'BaseCompositePile':
        pass

    @abstractmethod
    def _build_FEM(self):
            pass
    
    @classmethod
    @abstractmethod
    def from_segment(cls, segment: PileType) -> 'BaseCompositePile':
        pass