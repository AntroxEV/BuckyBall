# -*- coding: utf-8 -*-
"""
Shared base class for OpenSees p-y curve implementations.
Defines methods to set up p-y curves according with openseespy requirements, and to build the relevant FEM model in OpenSeesPy.
"""

from abc_pycurve import BasePYCurve
import numpy as np
import opsunixothermaterials as opsmat


class OpsBasePYCurve(BasePYCurve):
    def __init__(self, soil, pile):
        super().__init__(soil, pile)
        self.multimethod = None
        self.expected_ymax = np.full(len(self.pile._zlist), 0.15).tolist() if self.pile._zlist is not None else None

    def set_MultilinearApprx(self, multimethod: str = "log", ymax: float = 0.15) -> list:
        if ymax <= 0:
            raise ValueError("ymax must be greater than 0 for log spacing.")

        match multimethod:
            case "uniform":
                ycorner = [ymax / 4, ymax / 2, 3 * ymax / 4, ymax]
            case "log":
                ycorner = np.logspace(np.log10(ymax / 100), np.log10(ymax), num=4).tolist()
            case _:
                raise ValueError(f"Unsupported method: {multimethod}")

        self.multimethod = multimethod
        return ycorner

    def set_opsmat(self, mat_type: str, ylist: list, zdepth: float):
        if ylist is None or len(ylist) == 0:
            raise ValueError("ylist must be a non-empty list of y values.")

        if mat_type == "Multilinear":
            dp = self.pile.cross.equivbreadth
            if self.multimethod is None:
                ycorner = self.set_MultilinearApprx(multimethod="log", ymax=max(ylist))
            else:
                ycorner = self.set_MultilinearApprx(multimethod=self.multimethod, ymax=max(ylist))

            pload = []
            for y in ycorner:
                pload.append(self.calc_py(dp, y, zdepth))
            self.opsmat = opsmat.OPSUnixMatFactory.create("Multilinear", ycorner, pload)
        else:
            raise ValueError(f"Unsupported material type: {mat_type}")

    def set_expected_ymax(self,ymaxlist: list):
        '''
        set up a list of expected ymax values (must match pile depth points)
        from top to bottom pile
        '''
        if ymaxlist is None or len(ymaxlist) == 0:
            raise ValueError("ymaxlist must be a non-empty list of ymax values.")
        if len(ymaxlist) != len(self.pile._zlist):
            raise ValueError("Length of ymaxlist must match the number of depth points in the pile.")
        self.expected_ymax = ymaxlist

    def _build_FEM(self):
        tagm = self._registry.get_up_tag(self._model_name, "tagMat")
        self.opsmat.build_ops(tag=tagm)
        return tagm
