"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

from .noncvx_variable import NonCvxVariable
import cvxpy.lin_ops.lin_utils as lu
from cvxpy.constraints import SDP
import numpy as np
import scipy.sparse as sp

class Orthog(NonCvxVariable):
    """ A variable satisfying X^TX = I. """
    def __init__(self, size, *args, **kwargs):
        super(Orthog, self).__init__(size, size, *args, **kwargs)

    def init_z(self, random):
        """Initializes the value of the replicant variable.
        """
        self.z.value = np.zeros(self.size)

    def _project(self, matrix):
        """All singular values except k-largest (by magnitude) set to zero.
        """
        U, s, V = np.linalg.svd(matrix)
        s[:] = 1
        return U.dot(np.diag(s)).dot(V)

    # Constrain all entries to be the value in the matrix.
    def _restrict(self, matrix):
        return [self == matrix]

    def canonicalize(self):
        """Relaxation [I X; X^T I] is PSD.
        """
        obj, constr = super(Orthog, self).canonicalize()
        identity = sp.eye(self.size[0])
        identity = lu.create_const(identity, self.size, sparse=True)
        obj = lu.vstack([
            lu.hstack([identity, obj]),
            lu.hstack([lu.transpose(obj), identity]),
        ])
        constr.append(SDP(obj))
        return (obj, constr)
