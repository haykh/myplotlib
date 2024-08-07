__version__ = "1.4.0"

CUSTOM_CMAPS = []


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


def load(style=None, flavor="light", usetex=True):
    """
    `myplotlib.load`

    preload custom style

    args
    ----------
    style [None] ............. : style to load (options: None, 'fancy', 'mono', 'hershey')
    flavor ['light'] ......... : color flavor to load (options: 'light', 'dark')
    usetex [True] ............ : whether to use LaTeX (True/False)
    """
    import os
    from matplotlib import font_manager
    import matplotlib.pyplot as plt

    assert usetex or style != "fancy", "fancy style requires usetex=True"

    CMAP_DIR = os.path.join(os.path.dirname(__file__), "assets/colormaps")
    CMAPS = os.listdir(CMAP_DIR)
    for cmap in CMAPS:
        cmapname = os.path.join(CMAP_DIR, cmap)
        __InstallCmapFromCSV(cmapname)
    FONT_DIR = os.path.join(os.path.dirname(__file__), "assets/fonts")
    font_files = font_manager.findSystemFonts(fontpaths=[FONT_DIR])
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)
    if style is not None:
        MPLSTYLE_FILE = os.path.join(
            os.path.dirname(__file__), f"assets/{style}.{flavor}.mplstyle"
        )
        plt.style.use(MPLSTYLE_FILE)
    if usetex and not style == "fancy":
        LATEXSTILE_FILE = os.path.join(
            os.path.dirname(__file__), f"assets/latex.mplstyle"
        )
        plt.style.use(LATEXSTILE_FILE)
