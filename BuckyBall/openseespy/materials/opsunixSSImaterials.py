"""
Collection of OpenSeesPy uniaxial material classes with a unified factory/registry system.

This module defines Python classes corresponding to the uniaxial materials available
in OpenSeesPy (e.g., Concrete01, Steel01, Elastic, Hysteretic). Each material class
encapsulates the parameters required by its OpenSeesPy counterpart and registers
itself with the central MaterialFactory through the `@OpsUnixMatFactory.register(name)`
decorator.

The factory maintains a class-level registry mapping material names to their
implementations, allowing materials to be instantiated dynamically using:

    material = OpsUnixMatFactory.create("Concrete01", *args, **kwargs)

This design removes the need for large conditional or match-case dispatch blocks
and supports extensibility: new material types can be added simply by defining a
class and decorating it with `@OpsUnixMatFactory.register`. The module therefore
serves as a structured catalogue of OpenSeesPy materials and provides a consistent,
object-oriented interface for model-building workflows.

Example:
mat = OpsUnixMatFactory.create("Concrete01", -30, -0.002, -20, -0.006)
mat.build_ops(tag=1)

"""
import openseespy.opensees as ops
from BuckyBall.openseespy.materials.OPSunixmatfact import OpsUnixMatFactory
from typing import Optional

@OpsUnixMatFactory.register("PySimple1")
class PySimple1:
    def __init__(self, soilType: int, pult: float, Y50: float, Cd: float,*, c=0.0 ):
        self.soilType = soilType
        self.pult = pult
        self.Y50 = Y50
        self.Cd = Cd
        self.c = c

    def build_ops(self, tag):
        ops.uniaxialMaterial('PySimple1', tag, self.soilType, self.pult, self.Y50, self.Cd, c=self.c)

@OpsUnixMatFactory.register("TzSimple1")
class TzSimple1:
    def __init__(self, soilType: int, tult: float, z50: float,*, c=0.0 ):
        self.soilType = soilType
        self.tult = tult
        self.z50 = z50
        self.c = c

    def build_ops(self, tag):
        ops.uniaxialMaterial('TzSimple1', tag, self.soilType, self.tult, self.z50, c=self.c)

@OpsUnixMatFactory.register("QzSimple1")
class QzSimple1:
    def __init__(self, qzType: int, qult: float, z50: float,*, suction=0.0, c=0.0 ):
        self.qzType = qzType
        self.qult = qult
        self.z50 = z50
        if suction < 0.0:
            raise ValueError('Suction should be non-negative')
        elif suction >= 0.1:
            raise ValueError('Suction should be less than or equal to 0.1')
        else:
            self.suction = suction
        self.c = c

    def build_ops(self, tag):
        ops.uniaxialMaterial('QzSimple1', tag, self.qzType, self.qult, self.z50, suction=self.suction, c=self.c)

