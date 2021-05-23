import myplotlib.plots as myplt
import myplotlib

import matplotlib.pyplot as plt
import numpy as np

def __getAx(ax):
  if ax is None:
    fig, ax = plt.subplots()
  return ax

def testColormaps(ax=None):
  ax = __getAx(ax)
  with plt.style.context('default'):
    zz = [np.linspace(0, 1, 256)]
    pad = 0.3
    dy = (1 - pad) / (len(myplotlib.CUSTOM_CMAPS))
    pady = pad / (len(myplotlib.CUSTOM_CMAPS))
    for i, cm in enumerate(myplotlib.CUSTOM_CMAPS):
      y1, y2 = (pady * (i + 0.5) + dy * i, pady * (i + 0.5) + dy * (i + 1))
      ax.imshow(zz, extent=(0, 1, y1, y2), cmap=cm);
      ax.text(1.04, 0.5 * (y1 + y2), f"\'{cm}\'", va='center', ha='left')
    ax.set_ylim(0, 1);
    ax.axis('off');
    ax.set_title("extra colormaps")

def testColors(ax=None):
  ax = __getAx(ax)
  prop_cycle = plt.rcParams['axes.prop_cycle']
  colors = prop_cycle.by_key()['color']
  title = 'default color cycle'
  ax.set_title(title)
  for j, c in enumerate(colors):
    with plt.style.context('default'):
      v_offset = -(j / len(colors))
      th = np.linspace(0, 2*np.pi, 512)
      ax.plot(th, .1*np.sin(th) + v_offset, color=c, lw=2)
      ax.annotate("'C{}'".format(j), (0, v_offset),
                  xytext=(-1.5, 0),
                  ha='right',
                  va='center',
                  color=c,
                  textcoords='offset points',
                  family='monospace')
      ax.annotate("{!r}".format(c), (2*np.pi, v_offset),
                  xytext=(1.5, 0),
                  ha='left',
                  va='center',
                  color=c,
                  textcoords='offset points',
                  family='monospace')
    ax.axis('off')

def testScatter(ax=None):
  ax = __getAx(ax)
  myplt.scatter(ax, 
             np.random.random(100), np.random.random(100), 
             xlog=True, ylog=True, 
             s=(0.1 + np.random.random(100)) * 20, 
             c='C0', label='drunk points', marker='*')
  myplt.scatter(ax, 
             10**(np.random.random(100)*2 - 2), 10**(np.random.random(100)*2 - 2), 
             xlog=True, ylog=True, 
             s=(0.1 + np.random.random(100)) * 20, 
             c='C1', label='sober points', pady=1.5, padx=1.2,
             ylim=(1e-2, None), xlim=(1e-2, None))
  plt.legend(loc = 'lower left')
  ax.set_xlabel(r'some funny number $x^2/y$ [units]');
  ax.set_ylabel(r'other number $z_{\nu}$ [units]');
  
def testPlot(ax=None):
  ax = __getAx(ax)
  myplt.plot(ax, np.arange(100), 20 * (2 + np.sin(np.linspace(0, 20, 100)) + np.random.random(100)**5), 
             padx=1.2, pady=2, c='C4', ls=':');
  myplt.plot(ax, np.arange(100), 20 * (2 + np.sin(np.linspace(0, 20, 100)) + np.random.random(100)**5), 
             padx=1.2, pady=2, c='C2');
  ax.set_ylabel('probability [\%]')
  ax.set_xlabel('age [yr]')

def testErrorbar(ax=None):
  ax = __getAx(ax)
  x = np.linspace(0, 1000, 10)
  y = np.sin(x / 100)
  dy = np.random.random(len(x)) * (y + 1.5) / 3
  myplt.dataPlot(ax.errorbar, ax, x, y, yerr=dy, pady=2, 
              marker='o', markeredgecolor='w', markerfacecolor='C11', markeredgewidth=1.5)
  ax.set_xlabel('time [s]')
  ax.set_ylabel('my very accurately measured variable [ly]')
  
def testPlot2d(ax=None):
  ax = __getAx(ax)
  x = np.linspace(-3, 3, 240)
  y = np.linspace(-3, 3, 200)
  xx, yy = np.meshgrid(x, y)
  zz = (xx**2 - np.sin(xx * yy**3)) + 6 * np.exp(-(xx**2 + yy**2) / 0.2)
  myplt.plot2d(ax, x, y, zz, cmap='bipolar', centering='edge', padx=1.1, pady=1.1)
  ax.set_xlabel('landscape in $x$')
  ax.set_ylabel('landscape in $y$')

def testAll():
  myplotlib.load()
  fig = plt.figure(figsize=(12, 12))
  axshape = (3, 2)
  axi = 1

  ax = plt.subplot(*axshape, axi)
  testColors(ax)
  axi += 1

  ax = plt.subplot(*axshape, axi)
  testColormaps(ax)
  axi += 1

  ax = plt.subplot(*axshape, axi)
  testScatter(ax)
  axi += 1

  ax = plt.subplot(*axshape, axi)
  testPlot(ax)
  axi += 1

  ax = plt.subplot(*axshape, axi)
  testErrorbar(ax)
  axi += 1

  ax = plt.subplot(*axshape, axi)
  testPlot2d(ax)
  axi += 1

  plt.tight_layout()
