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
def __genericXYDataPlot(function, ax,
                        x, y, 
                        xlog=False, ylog=False, 
                        xlim=None, ylim=None,
                        padx=1.1, pady=1.1, 
                        **kwargs):
  function(x, y, **kwargs);
  xlim = __setMinMax(xlim, x)
  ylim = __setMinMax(ylim, y)
  ax.spines['bottom'].set_bounds(*xlim)
  ax.spines['left'].set_bounds(*ylim)
  if xlog:
    ax.set_xscale('log')
    x1, x2 = xlim
    ax.set_xlim(*list(map(lambda x: 10**x, __stretch(np.log10(x1), np.log10(x2), padx))))
  else:
    x1, x2 = xlim
    ax.set_xlim(*__stretch(x1, x2, padx))
  if ylog:
    ax.set_yscale('log')
    y1, y2 = ylim
    ax.set_ylim(*list(map(lambda x: 10**x, __stretch(np.log10(y1), np.log10(y2), pady))))
  else:
    y1, y2 = ylim
    ax.set_ylim(*__stretch(y1, y2, pady))

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
    
