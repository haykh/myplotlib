import matplotlib.pyplot as plt
import numpy as np
import myplotlib.plots as pl

def __getAx(ax):
  if ax is None:
    fig, ax = plt.subplots()
  return ax

def testScatter(ax=None):
  pl.scatter(ax, 
             np.random.random(100), np.random.random(100), 
             xlog=True, ylog=True, 
             s=(0.1 + np.random.random(100)) * 20, 
             c='C0', label='drunk points', marker='*')
  pl.scatter(ax, 
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
  pl.plot(ax, np.arange(100), 20 * (2 + np.sin(np.linspace(0, 20, 100)) + np.random.random(100)**5), 
             padx=1.2, pady=2, c='C4', ls=':');
  pl.plot(ax, np.arange(100), 20 * (2 + np.sin(np.linspace(0, 20, 100)) + np.random.random(100)**5), 
             padx=1.2, pady=2, c='C2');
  ax.set_ylabel('probability [\%]')
  ax.set_xlabel('age [yr]')
  ax.set_title('how likely you are to die?');

def testErrorbar(ax=None):
  ax = __getAx(ax)
  x = np.linspace(0, 1000, 10)
  y = np.sin(x / 100)
  dy = np.random.random(len(x)) * (y + 1.5) / 3
  pl.__genericXYDataPlot(ax.errorbar, ax, x, y, yerr=dy, pady=2, 
                         marker='o', markeredgecolor='w', markerfacecolor='C11', markeredgewidth=1.5)
  ax.set_xlabel('time [s]')
  ax.set_ylabel('my very accurately measured variable [ly]')
  
def testPlot2d(ax=None):
  ax = __getAx(ax)
  x = np.linspace(-3, 3, 240)
  y = np.linspace(-3, 3, 200)
  xx, yy = np.meshgrid(x, y)
  zz = (xx**2 - np.sin(xx * yy**3)) + 6 * np.exp(-(xx**2 + yy**2) / 0.2)
  pl.plot2d(ax, x, y, zz, cmap='bipolar', centering='edge', padx=1.1, pady=1.1)
  ax.set_xlabel('landscape in $x$')
  ax.set_ylabel('landscape in $y$')

def testAll():
  import myplotlib as myplt
  myplt.load()
  fig = plt.figure(figsize=(12, 12))
  ax = plt.subplot(221)
  testScatter(ax)
  ax = plt.subplot(222)
  testPlot(ax)
  ax = plt.subplot(223)
  testErrorbar(ax)
  ax = plt.subplot(224)
  testPlot2d(ax)
