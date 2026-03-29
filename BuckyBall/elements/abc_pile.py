# -*- coding: utf-8 -*-
"""
Abstract Class for Pile Properties and Methods.

@author: Dr Alessandro Tombari

-------------
"""
from abc import ABC, abstractmethod
from BuckyBall.shared.adc_cross_section import CrossSection
from BuckyBall.materials.adc_standardmat import UniaxialMaterial
from BuckyBall.shared.abc_modelregistry import ModelRegistry

class BasePile(ABC):
    """
    Abstract Class for Pile Properties and Methods.

    Parameters
    ----------
    L : float
        length of the pile [m]
    dz : float
        vertical discretization step for the pile [m]
    Zbtm: float
        depth of the pile tip [m]
    cross: CrossSection
        cross-sectional dataclass for properties of the pile (e.g., area, moment of inertia)  
    """

    def __init__(self, L: float, dz: float, Zbot: float, cross: CrossSection, material: UniaxialMaterial, *, XY: tuple | None = None):
        self.L = L
        self.dz = dz
        self.Zbtm = Zbot
        self.cross = cross
        self.material = material
        self._zlist: list | None = None #z-coordinates set during building
        self._nodetaglist: list | None = None #node tags set during building
        self._eletaglist: list | None = None #element tags set during building
        self.set_XY(XY)
        self._edges = (Zbot, Zbot + L)

    def __add__(self, other):
        if not isinstance(other, BasePile):
            return NotImplemented
        new_L = self.L + other.L
        new_dz = min(self.dz, other.dz)  # Use the smaller dz for finer discretization
        new_Zbtm = min(self.Zbtm, other.Zbtm)  # Use the shallower Zbtm for the combined pile
        new_cross = self.cross  # first object dominates
        new_material = self.material  # first object dominates
        new_XY = self._XY  # first object dominates
        return self._combine_with(new_L, new_dz, new_Zbtm, new_cross, new_material, new_XY=new_XY)


 
    def _get_sectional_properties(self) -> tuple:
        """Returns the cross-sectional properties of the pile.

        Returns
        -------
        tuple
            A tuple containing the following cross-sectional properties:
            - Ix: Moment of inertia about the x-axis [m^4]
            - Iy: Moment of inertia about the y-axis [m^4]
            - Jxy: Torsional constant [m^4]
            - A: Cross-sectional area [m^2]
            - As: Shear area [m^2]
            
        """
        return (self.cross.Ix, self.cross.Iy, self.cross.Jxy, self.cross.A, self.cross.As)

    def _get_material_properties(self) -> tuple:
        """Returns the material properties of the pile.

        Returns
        -------
        tuple
            A tuple containing the following material properties:
            - E: Young's modulus [Pa]
            - G: Shear modulus [Pa]
            - nu: Poisson's ratio [-]
        """
        return (self.material.Einit, self.material._Ginit, self.material.nu)
    
    def _discretize_pile(self) -> list:
        """Discretizes the pile into segments based on the specified length and discretization step.

        Returns
        -------
        list
            A list of depth values representing the discretized segments of the pile.
        """
        _zlist=[self.Zbtm + i * self.dz for i in range(0,int(self.L / self.dz) + 1)]
        if self.L % self.dz != 0:
            _zlist.append(self.Zbtm + self.L)  # Ensure the last node is at the pile tip
        return _zlist
    
    def _set_ModelRegistry(self, model_name: str, registry: ModelRegistry) -> None: 
        """set the singleton instance of the model registry.

        """
        self._model_name = model_name
        self._registry = registry
    
    def set_XY(self, xy: tuple | None) -> None:
        if xy is None:
            self._XY = (0.0, 0.0)
            return

        x = xy[0] if xy[0] is not None else 0.0
        y = xy[1] if xy[1] is not None else 0.0
        self._XY = (x, y)

    @abstractmethod
    def _build_FEM(self) -> None:
        """Abstract method to create the pile in the FEM solver. This method should be implemented by subclasses to define the specific behavior of the pile creation process.
        """
        pass

    @abstractmethod
    def _combine_with(self, new_L, new_dz, new_Zbtm, new_cross, new_material,new_XY) -> 'BasePile':
        """Combines this pile with another pile to create a new pile with properties that are a combination of the two.

        Parameters
        ----------
        new_L : float
            The length of the combined pile.
        new_dz : float
            The discretization step for the combined pile.
        new_Zbtm : float
            The bottom depth of the combined pile.
        new_cross : CrossSection
            The cross-sectional properties of the combined pile.
        new_material : Material
            The material properties of the combined pile.

        Returns
        -------
        BasePile
            A new pile that is a combination of this pile and the other pile.
        """
        ...
