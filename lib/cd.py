from typing import List
import numpy as np
import itertools
import sys
import time

def getBasis(n : int) -> List(np.ndarray):
  """
    Generate a `\mathbb{R}`-basis of the n-th CD-algebra.
  """
  basis = []
  for i in range(2 ** (n-1)):
    z = np.zeros( 2 ** (n-1), dtype=int)
    z[i] = 1
    basis.append(z)
    return basis

mtables = {}
def getMTable(n : int):
  if not n in mtables:
    basis = getBasis(n)
    for x in basis:
      for y in basis:
        indexX = tuple(x).index(1)
        indexY = tuple(y).index(1)
        mtables[n][(indexX,indexY)] = CDMult(x,y)
  return mtables[n]

def CDConj(x : np.ndarray) -> np.ndarray:
  """
    This is the conjugation operation on a Cayley-Dickson Algebra. The length of x
    determines the dimension of the algebra in which x resides.
  """
  n = len(x)

  if n == 1:
    return x

  m = n // 2
  a, b = x[:m], x[m:]
  z = np.zeros(n,dtype=int)
  z[:m] = CDConj(a)
  z[m:] = -1 * b
  return z

def CDMult(x : np.ndarray, y : np.ndarray) -> np.ndarray:
  """
    Verbatim implementation of the Cayley-Dickson algebra multiplication. Length
    of x determines dimension of the algebra. Therefore the length of x should
    match the length of y.
  """
  n = len(x)

  if n == 1:
    return x*y
  m = n // 2
  a, b = x[:m], x[m:]
  c, d = y[:m], y[m:]
  z = np.zeros(n, dtype=int)
  z[:m] = CDMult( a, c ) - CDMult( CDConj(d), b )
  z[m:] = CDMult( d, a ) + CDMult( b, CDConj(c) )
  return z

def CDBasisMult(x: np.ndarray, y: np.ndarray, mtable=None) -> np.ndarray:
  x_nonzeros, y_nonzeros = x.nonzero, y.nonzero
  index_x, index_y = x_nonzeros[0], y_nonzeros[0]
  if mtable is None:
    mtable = getMTable(len(x))
  return mtable[(index_x, index_y)]

def CDSmartMult(x: np.ndarray, y: np.ndarray, basis=False, mtable=None) -> np.ndarray:
  if basis:
    return CDBasisMult(x,y, mtable=mtable)
  else:
    return CDMult(x,y)

def commutator(x: np.ndarray, y: np.ndarray, **opts)-> np.ndarray:
  return CDSmartMult(x,y, opts) - CDSmartMult(y,x, opts)

def associator(x: np.ndarray, y: np.ndarray, z: np.ndarray, **opts) -> np.ndarray:
  return CDMult(x, CDMult(y,z,opts), opts) - CDMult(CDMult(x,y, opts), z, opts)

def commuAssociator(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray, **opts) -> np.ndarray:
  return (
    associator(commutator(a,b,opts),c,d,opts)
    - commutator(associator(a,b,c, opts),d, opts)
    + associator(commutator(d,b, opts),c,a, opts)
    - commutator(associator(d,b,c, opts),a, opts)
  )

def commuAssociatorAlt(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray, **opts) -> np.ndarray:
  """
    This is the `commuAssociator`, but the role of `b` and `c` are flipped in
    the last two terms.
  """
  return (
    associator(commutator(a,b,opts),c,d,opts)
    - commutator(associator(a,b,c, opts),d, opts)
    + associator(commutator(d,c, opts),b,a, opts)
    - commutator(associator(d,c,b, opts),a, opts)
  )
