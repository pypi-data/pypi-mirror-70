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
import cvxpy as cvx
import numpy as np

class Integer(NonCvxVariable):
    """ An integer variable. """
    # M - upper bound on |x|
    def __init__(self, rows=1, cols=1, M=None, *args, **kwargs):
        if M is None or np.any(M <= 0):
            raise Exception("Integer requires positive values for M.")
        self.M = np.floor(M)
        if np.isscalar(self.M) and (rows, cols) != (1,1):
            self.M = self.M*np.ones((rows,cols))
        super(Integer, self).__init__(rows, cols, *args, **kwargs)

    def init_z(self, random):
        """Initializes the value of the replicant variable.
        """
        self.z.value = np.zeros(self.shape)

    # All values set rounded to the nearest integer.
    def _project(self, matrix):
        return np.around(matrix)

    # Constrain all entries to be the value in the matrix.
    def _restrict(self, matrix):
        return [self == matrix]

    def _neighbors(self, matrix):
        neighbors_list = []
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                for diff in [1,-1]:
                    new_mat = matrix.copy()
                    new_mat[i,j] = new_mat[i,j] + diff
                    neighbors_list += [new_mat]
        return neighbors_list

    def relax(self):
        return [cvx.abs(self) <= self.M]
