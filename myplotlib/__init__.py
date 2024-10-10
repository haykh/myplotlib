__version__ = "1.5.0"


import os
import matplotlib.pyplot as plt
from matplotlib import font_manager

import myplotlib


def __RGBToPyCmap(rgbdata):
    import numpy as np

    nsteps = rgbdata.shape[0]
    stepaxis = np.linspace(0, 1, nsteps)
    rdata = []
    gdata = []
    bdata = []
    for istep in range(nsteps):
        r = rgbdata[istep, 0]
        g = rgbdata[istep, 1]
        b = rgbdata[istep, 2]
        rdata.append((stepaxis[istep], r, r))
        gdata.append((stepaxis[istep], g, g))
        bdata.append((stepaxis[istep], b, b))
    mpl_data = {"red": rdata, "green": gdata, "blue": bdata}
    return mpl_data


CUSTOM_CMAPS = []


def __InstallCmapFromCSV(csv):
    global CUSTOM_CMAPS
    import os
    import numpy as np
    import matplotlib as mpl

    cmap = os.path.splitext(os.path.basename(csv))[0]
    cmap_data = np.loadtxt(csv, delimiter=",")
    if cmap not in mpl.colormaps.keys():
        CUSTOM_CMAPS.append(cmap)
        mpl_data = __RGBToPyCmap(cmap_data)
        mpl.colormaps.register(
            cmap=mpl.colors.LinearSegmentedColormap(cmap, mpl_data, cmap_data.shape[0])
        )
    cmap = f"{cmap}_r"
    if cmap not in mpl.colormaps.keys():
        mpl_data_r = __RGBToPyCmap(cmap_data[::-1, :])
        mpl.colormaps.register(
            cmap=mpl.colors.LinearSegmentedColormap(
                cmap, mpl_data_r, cmap_data.shape[0]
            )
        )


myplotlib_path = myplotlib.__path__[0]
styles_path = os.path.join(myplotlib_path, "assets")

stylesheets = {}
for folder, _, _ in os.walk(styles_path):
    new_stylesheets = plt.style.core.read_style_directory(folder)
    stylesheets.update(new_stylesheets)

plt.style.core.update_nested_dict(plt.style.library, stylesheets)
plt.style.core.available[:] = sorted(plt.style.library.keys())

CMAP_DIR = os.path.join(myplotlib_path, "assets/colormaps")
CMAPS = os.listdir(CMAP_DIR)
for cmap in CMAPS:
    cmapname = os.path.join(CMAP_DIR, cmap)
    __InstallCmapFromCSV(cmapname)
FONT_DIR = os.path.join(myplotlib_path, "assets/fonts")
font_files = font_manager.findSystemFonts(fontpaths=[FONT_DIR])
for font_file in font_files:
    font_manager.fontManager.addfont(font_file)
