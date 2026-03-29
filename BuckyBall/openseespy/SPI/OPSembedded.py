# -*- coding: utf-8 -*-
"""
Concrete Class for Embedded Piles for OpenSeesPy. 
This class inherits from the BasePile class and SPI (container)
 and implements the build_FEM method
 to create the pile elements in OpenSeesPy and the py/qz/tz springs
It is a generic wrapper to add soil-pile interaction elements to the pile elements.

@author: Dr Alessandro Tombari

"""
from BuckyBall.SPI.abc_embedded import BaseEmbedded
import openseespy.opensees as ops
from BuckyBall.openseespy.materials import opsunixothermaterials, opsunixstandmaterials,opsunixSSImaterials
from BuckyBall.openseespy.materials.OPSunixmatfact import OpsUnixMatFactory

class Embedded(BaseEmbedded):

    #def set_opsconstbehavior(self, unixmatname: str):
        #self.material = OpsUnixMatFactory.create(unixmatname)

    def _update_matprop(self,citem) -> None:
        _XYZ = self.material.XYZ
        if _XYZ is not None:
            X=_XYZ[0] if len(_XYZ) > 0 else 0.0 #_XYZ must be len 3 or None
            Y=_XYZ[1] if len(_XYZ) > 1 else 0.0
            Z=self.Zbtm
            self.material.XYZ=(X,Y,Z)
            self.material.updateProp()
        else: 
            X=0.0
            Y=0.0
            Z=0.0 

    def _add_soil_pile_interaction(self):
        _zlist = self._cpile._zlist
        if _zlist is None: raise ValueError("Pile has not been created correctly")
        _ntagpile = self._cpile._nodetaglist
        if _ntagpile is None: raise ValueError("Pile has not been created corretly")
        xpile = self._cpile._XY[0]
        ypile = self._cpile._XY[1]
        item_list = self._cspi._items

        _nytag = []
        _qztag = []
        _tztag = []
        for indx, item in enumerate(item_list):
            if item is not None:
                match indx:
                    case 0: #create nodes for py_x curve
                        self._build_py_x(xpile,ypile,_zlist,_ntagpile)
                    case 1: #create nodes for py_y curve
                        self._build_py_y(xpile,ypile,_zlist,_ntagpile)
                    case 2: #create nodes for qz curve
                        pass
                    case 3: #create nodes for tz curve
                        pass
                    case _:
                        raise ValueError("Invalid index in item list - BUG")
        
                    

    def _build_py_x(self,xpile,ypile,zlist,ntagpile):
        _reg = self._cpile._registry #registry is create and set by the Model
        _mname = self._cpile._model_name
        _cpyx = self._cspi.get_py_x()
        if _cpyx is None: raise ValueError("PY curve is None, problem in SPIContainer - BUG")
        _nxtag = []
        _mattag = []
        if _cpyx.expected_ymax is None: raise ValueError("Expected ymax is None, problem in PY curve - BUG")
        for indz, zi in enumerate(zlist):
            _ntag=_reg.get_up_tag(_mname, "tagNode")
            _nxtag.append(_ntag)
            ops.node(_ntag,xpile-1.0,ypile,zi) #create node on the left
            ops.fix(_ntag, *(1,1,1,1,1,1)) #fix the node in all DOF
            _cpyx.set_opsmat("Multilinear", _cpyx.expected_ymax[indz], zi) #set the material properties for the py curve - this will create the material in OpenSeesPy
            _mattag.append(_cpyx._build_FEM()) #build the material in OpenSeesPy - this will create the material in OpenSeesPy and set the tagMat in the registry
        # uniaxialMaterial('MultiLinear', matTag, *pts)

        if len(ntagpile) != len(_nxtag):
            raise ValueError("Side nodes not equal pile nodes - BUG")
        #element('twoNodeLink', eleTag, *eleNodes, '-mat', *matTags, '-dir', *dir, <'-orient', *vecx, *vecyp>, <'-pDelta', *pDeltaVals>, <'-shearDist', *shearDist>, <'-doRayleigh'>, <'-mass', m>)
        for indnx,tag in enumerate(_nxtag):
            _tagEle=_reg.get_up_tag(_mname, "tagEle")
            ops.element('twoNodeLink', _tagEle, *(_nxtag,ntagpile[indnx]), '-mat',_mattag[indnx] ,'-dir',1) 

    
    def _build_py_y(self,xpile,ypile,zlist,ntagpile):
        _reg = self._cpile._registry #registry is create and set by the Model
        _mname = self._cpile._model_name
        _cpyy = self._cspi.get_py_y()
        if _cpyy is None: raise ValueError("PY curve is None, problem in SPIContainer - BUG")
        _nxtag = []
        _mattag = []
        if _cpyy.expected_ymax is None: raise ValueError("Expected ymax is None, problem in PY curve - BUG")
        for indz, zi in enumerate(zlist):
            _ntag=_reg.get_up_tag(_mname, "tagNode")
            _nxtag.append(_ntag)
            ops.node(_ntag,xpile,ypile-1.0,zi) #create node on the left
            ops.fix(_ntag, *(1,1,1,1,1,1)) #fix the node in all DOF
            _cpyy.set_opsmat("Multilinear", _cpyy.expected_ymax[indz], zi) #set the material properties for the py curve - this will create the material in OpenSeesPy
            _mattag.append(_cpyy._build_FEM()) #build the material in OpenSeesPy - this will create the material in OpenSeesPy and set the tagMat in the registry
        # uniaxialMaterial('MultiLinear', matTag, *pts)

        if len(ntagpile) != len(_nxtag):
            raise ValueError("Side nodes not equal pile nodes - BUG")
        #element('twoNodeLink', eleTag, *eleNodes, '-mat', *matTags, '-dir', *dir, <'-orient', *vecx, *vecyp>, <'-pDelta', *pDeltaVals>, <'-shearDist', *shearDist>, <'-doRayleigh'>, <'-mass', m>)
        for indnx,tag in enumerate(_nxtag):
            _tagEle=_reg.get_up_tag(_mname, "tagEle")
            ops.element('twoNodeLink', _tagEle, *(_nxtag,ntagpile[indnx]), '-mat',_mattag[indnx] ,'-dir',1) 

    
    def _build_FEM(self):
        _pile=self._cpile
        _spi=self._cspi
        _pile._build_FEM()
        self._add_soil_pile_interaction()






