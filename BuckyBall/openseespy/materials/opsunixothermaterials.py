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
from BuckyBall.openseespy.materials.OPSunixmatfact import OpsUnixMatFactory
from typing import Optional

@OpsUnixMatFactory.register("MultiLinear")
class MultiLinear:
    def __init__(self, strain: list, stress: list):
        if len(strain) > 4 or len(stress) > 4:
            raise ValueError('max 4 stress and 4 strain values could be defined')
        if len(strain) != len(stress):
            raise ValueError('strain and stress must have the same number of (ordered) elements')
        
        self._pts = [x for idx in range(0,len(strain)) for x in (strain[idx], stress[idx])]
    

    def build_ops(self, tag):
        ops.uniaxialMaterial('MultiLinear', tag, self._pts)




