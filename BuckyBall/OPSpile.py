# -*- coding: utf-8 -*-
"""
Concrete Class for Pile.

@author: Dr Alessandro Tombari


-------------
"""
from abc_pile import BasePile
import openseespy.opensees as ops
TRANSF_TAG = 1

class OpsPile(BasePile):

    def set_opselement(self, element_type: str):
        match element_type:
            case "elasticBeamColumn":
                self._element_type = "elasticBeamColumn"
            case "TimoshenkoBeamColumn":
                self._element_type = "TimoshenkoBeamColumn"
            case "dispBeamColumn":
                self._element_type = "dispBeamColumn"
            case "forceBeamColumn":
                self._element_type = "forceBeamColumn"
            case _:
                self._element_type = "elasticBeamColumn"  # Default to elasticBeamColumn if not specified
                raise ValueError(f"Unsupported element type: {element_type}. Supported types are: 'elasticBeamColumn' (Default), 'TimoshenkoBeamColumn', 'dispBeamColumn', 'forceBeamColumn'.")

    def _add_element(self, element_type: str, tagele: int, inode: int):
        match self._element_type:
            case "elasticBeamColumn": #element('elasticBeamColumn', eleTag, *eleNodes, Area, E_mod, G_mod, Jxx, Iy, Iz, transfTag, <'-mass', mass>, <'-cMass'>)
                ops.element("elasticBeamColumn", tagele, inode, inode+1, self.cross.A, self.material.Einit, self.material._Ginit, self.cross.Jxy, self.cross.Ix, self.cross.Iy, TRANSF_TAG,'-mass', self.cross.A*self.material.rho)
            case "TimoshenkoBeamColumn": #element('ElasticTimoshenkoBeam', eleTag, *eleNodes, E_mod, G_mod, Area, Jxx, Iy, Iz, Avy, Avz, transfTag, <'-mass', massDens>, <'-cMass'>)
                ops.element("ElasticTimoshenkoBeam", tagele, inode, inode+1, self.material.Einit, self.material._Ginit, self.cross.A, self.cross.Jxy, self.cross.Ix, self.cross.Iy, self.cross.As, self.cross.As, TRANSF_TAG,'-mass', self.cross.A*self.material.rho)
            case "dispBeamColumn":
                NotImplementedError("dispBeamColumn element type is not yet implemented.")
            case "forceBeamColumn":
                NotImplementedError("forceBeamColumn element type is not yet implemented.")
            case _:
                #self._element_type = "elasticBeamColumn"  # Default to elasticBeamColumn if not specified
                raise ValueError(f"Unsupported element type: {element_type}. Supported types are: 'elasticBeamColumn' (Default), 'TimoshenkoBeamColumn', 'dispBeamColumn', 'forceBeamColumn'.")
 

    def _build_FEM(self):
        xy = self._XY
        _mname = self._model_name
        if _mname is None:
            raise ValueError("Model name is not set. Use OPSGateway to build the OpenseesPy Model.")
        _reg= self._registry
        if _reg is None:
            raise ValueError("Model registry is not set. Use OPSGateway to build the OpenseesPy Model.")
        self._zlist=self._discretize_pile()
        _taglist=[]
        _elelist=[]
        for i in range(len(self._zlist)):
            _ntag=_reg.get_up_tag(_mname, "tagNode")
            _taglist.append(_ntag)
            ops.node(_ntag,xy[0],xy[1],self._zlist[i])
        self._nodetaglist = _taglist
        for i in range(0,len(_taglist)-1):
            _tagEle=_reg.get_up_tag(_mname, "tagEle")
            _elelist.append(_tagEle)
            self._add_element(self._element_type, _tagEle, _taglist[i])
        self._eletaglist = _elelist

