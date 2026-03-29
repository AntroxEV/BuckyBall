# -*- coding: utf-8 -*-
"""
Concrete Class for Composite Pile.

@author: Dr Alessandro Tombari


-------------
"""

from BuckyBall.elements.abc_compositepile import BaseCompositePile
from BuckyBall.openseespy.elements.OPSpile import Pile
from BuckyBall.openseespy.SPI.OPSembedded import Embedded
from typing import TypeVar, Union, List

OpsPile=TypeVar('OpsPile', bound=Pile)
OpsEmbedded=TypeVar('OpsEmbedded', bound=Embedded)
PileType=Union[OpsPile, OpsEmbedded]

class CompositePile(BaseCompositePile):

    def _combine_with(self, new_segments: List[PileType]) -> 'CompositePile':
        return CompositePile(new_segments)

    def _build_FEM(self):
        for seg in self._segments:
            seg._build_FEM()

    @classmethod
    def from_segment(cls, segment: PileType) -> 'CompositePile' :
        if not isinstance(segment, (Pile, Embedded)):
            raise TypeError("Segment must be an instance of Pile or Embedded Pile.")
        return cls([segment])
    
    