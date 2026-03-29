"""
Collection of OpenSeesPy uniaxial material classes with a unified factory/registry system.

This module defines Python classes corresponding to the uniaxial materials available
in OpenSeesPy (e.g., Concrete01, Steel01, Elastic, Hysteretic). Each material class
encapsulates the parameters required by its OpenSeesPy counterpart and registers
itself with the central MaterialFactory through the `@OPSUnixMatFactory.register(name)`
decorator.

The factory maintains a class-level registry mapping material names to their
implementations, allowing materials to be instantiated dynamically using:

    material = OPSUnixMatFactory.create("Concrete01", *args, **kwargs)

This design removes the need for large conditional or match-case dispatch blocks
and supports extensibility: new material types can be added simply by defining a
class and decorating it with `@OPSUnixMatFactory.register`. The module therefore
serves as a structured catalogue of OpenSeesPy materials and provides a consistent,
object-oriented interface for model-building workflows.

Example:
mat = OPSUnixMatFactory.create("Concrete01", -30, -0.002, -20, -0.006)
mat.build_ops(tag=1)

"""
import openseespy.opensees as ops
from OPSunixmatfact import OPSUnixMatFactory
from typing import Optional

@OPSUnixMatFactory.register("Elastic")
class Elastic:
    def __init__(self, E0: float,*,eta: float = 0.0, Eneg: Optional[float] = None):
        self.E0 = E0
        self.eta = eta  
        if Eneg is None:
            self.Eneg = E0
        else:
            self.Eneg = Eneg
        if self.E0 < 0.0:
            raise ValueError('Elastic Modulus E0 should be non-negative')


    def build_ops(self, tag):
        ops.uniaxialMaterial('Elastic', tag, self.E0, self.eta, self.Eneg)

@OPSUnixMatFactory.register("ElasticPP")
class ElasticPP:
    def __init__(self, E0: float,epsyP: float,*,eps0: float = 0.0, epsyN: Optional[float] = None):
        self.E0 = E0
        self.epsyP = epsyP
        self.eps0 = eps0
        if epsyN is None:
            self.epsyN = epsyP
        else:
            self.epsyN = epsyN
        if self.E0 < 0.0:
            raise ValueError('Elastic Modulus E0 should be non-negative')


    def build_ops(self, tag):
        ops.uniaxialMaterial('ElasticPP', tag, self.E0, self.epsyP, self.epsyN, self.eps0)

@OPSUnixMatFactory.register("ElasticPPGap")
class ElasticPPGap:
    def __init__(self, E0: float, Fy: float, gap: float,*,eta: float = 0.0, damage: Optional[str] = 'noDamage'):
        self.E0 = E0
        self.Fy = Fy
        self.gap = gap
        self.eta = eta
        self.damage = damage
        if damage is not None and damage not in ['noDamage', 'damage']:
            raise ValueError('Invalid damage option. Choose from "noDamage", or "damage".')
        if self.E0 < 0.0:
            raise ValueError('Elastic Modulus E0 should be non-negative')

    def build_ops(self, tag):
        ops.uniaxialMaterial('ElasticPPGap', tag, self.E0, self.Fy, self.gap, self.eta, self.damage)
