"""
Dimensional analysis primitives.
"""
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Dimension:
    """Dimensional signature: (L, M, T, ...)."""
    L: int = 0  # length
    M: int = 0  # mass
    T: int = 0  # time
    K: int = 0  # temperature
    A: int = 0  # current

    def __mul__(self, other): return Dimension(*[a+b for a,b in zip(self,other)])
    def __truediv__(self, other): return Dimension(*[a-b for a,b in zip(self,other)])
    def __pow__(self, n): return Dimension(*[a*n for a in self])
    def __iter__(self): yield from (self.L, self.M, self.T, self.K, self.A)


DIMENSIONLESS = Dimension()
LENGTH        = Dimension(L=1)
TIME          = Dimension(T=1)
MASS          = Dimension(M=1)
VELOCITY      = Dimension(L=1, T=-1)
ENERGY        = Dimension(M=1, L=2, T=-2)
FORCE         = Dimension(M=1, L=1, T=-2)
