def __RGBToPyCmap(rgbdata):
  import numpy as np
  nsteps = rgbdata.shape[0]
  stepaxis = np.linspace(0, 1, nsteps)
  rdata=[]; gdata=[]; bdata=[]
  for istep in range(nsteps):
    r = rgbdata[istep,0]
    g = rgbdata[istep,1]
    b = rgbdata[istep,2]
    rdata.append((stepaxis[istep], r, r))
    gdata.append((stepaxis[istep], g, g))
    bdata.append((stepaxis[istep], b, b))
  mpl_data = {'red':   rdata,
              'green': gdata,
              'blue':  bdata}
  return mpl_data

def __InstallCmapFromCSV(csv):
  import os
  import numpy as np
  import matplotlib as mpl
  import matplotlib.pyplot as plt
  cmap = os.path.splitext(os.path.basename(csv))[0]
  cmap_data = np.loadtxt(csv, delimiter=',')
  mpl_data = __RGBToPyCmap(cmap_data)
  plt.register_cmap(cmap=mpl.colors.LinearSegmentedColormap(cmap, mpl_data, cmap_data.shape[0]))
  mpl_data_r = __RGBToPyCmap(cmap_data[::-1,:])
  plt.register_cmap(cmap=mpl.colors.LinearSegmentedColormap(f'{cmap}_r', mpl_data_r, cmap_data.shape[0]))

def load():
  import os
  import pkg_resources
  from matplotlib import font_manager
  import matplotlib.pyplot as plt
  CMAP_DIR = pkg_resources.resource_filename(__name__, 'assets/colormaps')
  CMAPS = pkg_resources.resource_listdir(__name__, 'assets/colormaps')
  for cmap in CMAPS:
    __InstallCmapFromCSV(os.path.join(CMAP_DIR, cmap))

  FONT_DIR = pkg_resources.resource_filename(__name__, 'assets/fonts')
  font_files = font_manager.findSystemFonts(fontpaths=[FONT_DIR])
  for font_file in font_files:
    font_manager.fontManager.addfont(font_file)

  MPLSTYLE_FILE = pkg_resources.resource_stream(__name__, 'assets/my.mplstyle')
  plt.style.use(MPLSTYLE_FILE.name)
