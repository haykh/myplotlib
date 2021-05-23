# . . . . .
# Credits to Patrick Crumley (@pcrumley)
# https://github.com/pcrumley/tristanUtils/blob/master/src/lic_NUMBA.py
# . . . . . 

# A NUMBA based implementation of the code found here:
# https://scipy-cookbook.readthedocs.io/items/LineIntegralConvolution.html
import numpy as np
from numpy import ones
from numba import jit, guvectorize, float64, int32

def generate_kernel(klen):
  kernel = np.sin(np.arange(klen) * np.pi / klen)
  return kernel.astype(np.float64)

def generate_texture(shape, seed=None):
  if seed is not None:
    np.random.seed(seed)
  return np.random.rand(*shape).astype(np.float64)

@jit
def advance(vx, vy, xyArr, fxfyArr, w, h):
  if vx>=0:
    tx = (1-fxfyArr[1])/vx
  else:
    tx = -fxfyArr[1]/vx
  if vy>=0:
    ty = (1-fxfyArr[0])/vy
  else:
    ty = -fxfyArr[0]/vy
  if tx<ty:
    if vx>=0:
      xyArr[1]+=1
      fxfyArr[1]=0
    else:
      xyArr[1]-=1
      fxfyArr[1]=1
    fxfyArr[0]+=tx*vy
  else:
    if vy>=0:
      xyArr[0]+=1
      fxfyArr[0]=0
    else:
      xyArr[0]-=1
      fxfyArr[0]=1
    fxfyArr[1]+=ty*vx
  if xyArr[1]>=w:
    xyArr[1]=w-1 # FIXME: other boundary conditions?
  if xyArr[1]<0:
    xyArr[1]=0 # FIXME: other boundary conditions?
  if xyArr[0]<0:
    xyArr[0]=0 # FIXME: other boundary conditions?
  if xyArr[0]>=h:
    xyArr[0]=h-1 # FIXME: other boundary conditions?


@jit(nopython=True)
def line_integral_convolution(vx, vy, texture, kernel):
  h = vx.shape[0]
  w = vx.shape[1]
  kernellen = kernel.shape[0]
  if h!=vy.shape[0] or w != vy.shape[1] :
    raise ValueError('Vx and Vy must the same shape')
  if h!=texture.shape[0] or w != texture.shape[1] :
    raise ValueError('The texture must have the same shape as the vectors')
  result = np.zeros((h,w),dtype=np.float32)

  xyArr = np.ones(2, dtype=np.int32)
  fxfyArr = np.empty(2, dtype=np.float64)
  for i in range(h):
    for j in range(w):
      xyArr[0] = i
      xyArr[1] = j
      fxfyArr[0] = 0.5
      fxfyArr[1] = 0.5

      k = kernellen//2
      result[i,j] += kernel[k]*texture[xyArr[0],xyArr[1]]
      while k<kernellen-1:
        advance(vx[xyArr[0],xyArr[1]],vy[xyArr[0],xyArr[1]],
                xyArr, fxfyArr, w, h)
        k+=1
        result[i,j] += kernel[k]*texture[xyArr[0],xyArr[1]]
      xyArr[0] = i
      xyArr[1] = j
      fxfyArr[0] = 0.5
      fxfyArr[1] = 0.5

      while k>0:
        advance(vx[xyArr[0],xyArr[1]],vy[xyArr[0],xyArr[1]],
                xyArr, fxfyArr, w, h)
        k-=1
        result[i,j] += kernel[k]*texture[xyArr[0],xyArr[1]]
  return result
