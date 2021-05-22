import numpy as np

def __stretch(left, right, pad):
  c = 0.5 * (left + right)
  d = 0.5 * (right - left)
  return (c - d * pad, c + d * pad)

def __setMinMax(lims, data):
  if not lims:
    lims = (np.min(data), np.max(data))
  if lims[0] == None:
    lims = (np.min(data), lims[1])
  if lims[1] == None:
    lims = (lims[0], np.max(data))
  return lims

def __setAxLims(ax, coords, log, pad, lim, spines):
  lim = __setMinMax(lim, coords)
  ax.spines[spines].set_bounds(*lim)
  if (spines == 'bottom'):
    func_setscale = ax.set_xscale
    func_setlim = ax.set_xlim
  elif (spines == 'left'):
    func_setscale = ax.set_yscale
    func_setlim = ax.set_ylim
  else:
    raise ValueError
  if log:
    func_setscale('log')
    p1, p2 = lim
    func_setlim(*list(map(lambda p: 10**p, __stretch(np.log10(p1), np.log10(p2), pad))))
  else:
    p1, p2 = lim
    func_setlim(*__stretch(p1, p2, pad))

def __genericXYDataPlot(function, ax,
                        x, y, 
                        xlog=False, ylog=False, 
                        xlim=None, ylim=None,
                        padx=1.1, pady=1.1, 
                        **kwargs):
  function(x, y, **kwargs);
  __setAxLims(ax, x, xlog, padx, xlim, 'bottom')
  __setAxLims(ax, y, ylog, pady, ylim, 'left')

def __checkDimensions2d(x, y, zz):
  x, y, zz = (np.array(np.squeeze(x)), np.array(np.squeeze(y)), np.array(np.squeeze(zz)))
  readShapes = f"`x.shape={x.shape}`, `y.shape={y.shape}`, `zz.shape={zz.shape}`"
  assert len(x.shape) == len(y.shape), f"Shapes of `x` and `y` must be of the same dimension: {readShapes}."
  assert len(zz.shape) == 2, f"`zz` must have exactly 2 non-trivial axes: {readShapes}."
  assert zz.shape[1] == x.shape[0], f"incompatible dimensions between `x` and `zz`: {readShapes}."
  assert zz.shape[0] == y.shape[0], f"incompatible dimensions between `y` and `zz`: {readShapes}."
  return (x, y, zz)

def __findExtent(x, y, centering):
  if centering == 'edge':
    dx = (x[1] - x[0]); dy = (y[1] - y[0])
    extent = (x.min(), x.max() + dx, y.min(), y.max() + dy)
  elif centering == 'center':
    dx = (x[1] - x[0]); dy = (y[1] - y[0])
    extent = (x.min() - dx*0.5, x.max() + dx*0.5, y.min() - dy*0.5, y.max() + dy*0.5)
  else:
    raise ValueError
  return extent

def scatter(ax, x, y, 
            xlog=False, ylog=False, 
            xlim=None, ylim=None,
            padx=1.1, pady=1.1, **kwargs):
  """
  add a scatter plot to a given axis

  args
  ----------
  ax .......................... : matplotlib axis object
  x, y ........................ : 1d data arrays
  xlog [False], ylog [False] .. : use log in x or y direction
  xlim [None], ylim [None] .... : tuples of x and y limits (None = determine from data)
  padx [1.1], pady [1.1] ...... : add whitespace to axes in each direction (1 = no additional space)
  **kwargs .................... : standard matplotlib kwargs passed to `ax.scatter`
  """
  __genericXYDataPlot(ax.scatter, ax, x, y, xlog, ylog, xlim, ylim, padx, pady, **kwargs)
    
def plot(ax, x, y, 
         xlog=False, ylog=False, 
         xlim=None, ylim=None,
         padx=1.1, pady=1.1, **kwargs):
  """
  add a simple plot to a given axis

  args
  ----------
  ax .......................... : matplotlib axis object
  x, y ........................ : 1d data arrays
  xlog [False], ylog [False] .. : use log in x or y direction
  xlim [None], ylim [None] .... : tuples of x and y limits (None = determine from data)
  padx [1.1], pady [1.1] ...... : add whitespace to axes in each direction (1 = no additional space)
  **kwargs .................... : standard matplotlib kwargs passed to `ax.scatter`
  """
  __genericXYDataPlot(ax.plot, ax, x, y, xlog, ylog, xlim, ylim, padx, pady, **kwargs)
    
def plot2d(ax, x, y, zz, 
           centering='edge', 
           xlim=None, ylim=None, 
           padx=1.1, pady=1.1,
           cbar='5%', cbar_pad=0.05,
           **kwargs):
  """
  add a 2d plot to a given axis

  args
  ----------
  ax .......................... : matplotlib axis object
  x, y ........................ : 1d or 2d arrays of coordinates
  centering ['edge'] .......... : centering of x & y nodes for the data ('edge', 'center')
  xlim [None], ylim [None] .... : tuples of x and y limits (None = determine from x & y)
  padx [1.1], pady [1.1] ...... : add whitespace to axes in each direction (1 = no additional space)
  cbar ['5%'] ................. : size of the colorbar in percent of x-axis (None = no colorbar) 
  cbar_pad [0.05] ............. : padding of the colorbar
  **kwargs .................... : standard matplotlib kwargs passed to `ax.scatter`
  """
  from mpl_toolkits.axes_grid1 import make_axes_locatable
  import matplotlib.pyplot as plt
  x, y, zz = __checkDimensions2d(x, y, zz)
  ax.grid(False)
  extent = __findExtent(x, y, centering)
  ax.imshow(zz, origin='lower', extent=extent, **kwargs)
  __setAxLims(ax, np.linspace(extent[0], extent[1]), False, padx, xlim, 'bottom')
  __setAxLims(ax, np.linspace(extent[2], extent[3]), False, pady, ylim, 'left')
  if cbar is not None:
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size=cbar, pad=cbar_pad)
    plt.colorbar(ax.get_images()[0], cax=cax)
