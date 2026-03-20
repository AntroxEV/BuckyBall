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


@OPSUnixMatFactory.register("Concrete01")
class Concrete01:
    def __init__(self, fpc, epsc0, fpcu, epsU):
        self.fpc = fpc
        self.epsc0 = epsc0
        self.fpcu = fpcu
        self.epsU = epsU

    def build_ops(self, tag):
        ops.uniaxialMaterial("Concrete01", tag,
                         self.fpc, self.epsc0, self.fpcu, self.epsU)





