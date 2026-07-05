"""Register bundled Matplotlib styles, colormaps, and fonts.

Importing `myplotlib` adds package assets to Matplotlib's style library,
colormap registry, and font manager.
"""

__version__ = "1.9.0"


import logging
import warnings
from pathlib import Path
from typing import Literal, Sequence, cast
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc_params_from_file
import matplotlib.colors as mcolors


myplotlib_path = str(Path(__file__).resolve().parent)
styles_path = str(Path(myplotlib_path) / "assets" / "styles")

CMAP_DIR = str(Path(myplotlib_path) / "assets" / "colormaps")
CMAPS = []

FONT_DIR = str(Path(myplotlib_path) / "assets" / "fonts")
font_files = []

_ASSETS_REGISTERED = False

_STYLE_RECIPES = {
    "fancy.light": [
        "_base",
        "_ticksout.base",
        "_fonts.garamond",
        "_palette.fancy.light",
    ],
    "fancy.dark": [
        "_base",
        "_ticksout.base",
        "_fonts.garamond",
        "_palette.fancy.dark",
        "_theme.fancy.dark",
    ],
    "classic.light": [
        "_base",
        "_ticksin.base",
        "_extraticks.base",
        "_fonts.classic",
        "_palette.classic.light",
    ],
    "classic.dark": [
        "_base",
        "_ticksin.base",
        "_extraticks.base",
        "_fonts.classic",
        "_palette.classic.dark",
        "_theme.classic.dark",
    ],
    "mono.light": [
        "_base",
        "_ticksout.base",
        "_fonts.mono",
        "_palette.mono",
    ],
    "mono.dark": [
        "_base",
        "_ticksout.base",
        "_fonts.mono",
        "_palette.mono",
        "_theme.mono.dark",
    ],
    "guttenberg.light": [
        "_base",
        "_ticksout.base",
        "_fonts.operina",
        "_style.guttenberg",
        "_palette.guttenberg.light",
        "_theme.guttenberg.light",
    ],
    "guttenberg.dark": [
        "_base",
        "_ticksout.base",
        "_fonts.operina",
        "_style.guttenberg",
        "_palette.guttenberg.dark",
        "_theme.guttenberg.dark",
    ],
    "soviet": [
        "_base",
        "_ticksin.base",
        "_fonts.literaturnaya",
        "_style.soviet",
    ],
    "latex": [
        "_base",
        "_style.latex",
    ],
}


class _MatplotlibNoiseFilter(logging.Filter):
    """Drop benign Matplotlib font and TeX log spam."""

    _TEXT_SNIPPETS = (
        "No TeX to Unicode mapping",
        "No Unicode mapping for",
        "findfont",
        "does not have a glyph for",
    )

    def filter(self, record):
        message = record.getMessage()
        return not any(snippet in message for snippet in self._TEXT_SNIPPETS)


def _quiet_matplotlib_warnings():
    """Suppress noisy Matplotlib diagnostics emitted during normal rendering."""
    noise_filter = _MatplotlibNoiseFilter()
    for logger_name in (
        "matplotlib.font_manager",
        "matplotlib.dviread",
        "matplotlib.mathtext",
        "matplotlib.texmanager",
        "matplotlib.backends.backend_pdf",
    ):
        logging.getLogger(logger_name).addFilter(noise_filter)

    warnings.filterwarnings(
        "ignore",
        message=r".*(No TeX to Unicode mapping|No Unicode mapping for).*",
        module=r"matplotlib\..*",
    )


def __RGBToPyCmap(rgbdata):
    """Convert RGB samples into a Matplotlib segmented colormap dictionary.

    Args
    ----
    rgbdata : NDArray
        Array of RGB samples with shape `(n, 3)` and values on `[0, 1]`.

    Returns
    -------
    dict[Literal['red', 'green', 'blue', 'alpha'], Sequence[tuple[float, ...]]]
        Segmented colormap channel data accepted by `LinearSegmentedColormap`.
    """
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
    mpl_data = {
        "red": rdata,
        "green": gdata,
        "blue": bdata,
    }
    return cast(
        dict[
            Literal["red", "green", "blue", "alpha"],
            Sequence[tuple[float, ...]],
        ],
        mpl_data,
    )


CUSTOM_CMAPS = []


def __InstallCmapFromCSV(csv):
    """Register a CSV colormap and its reversed variant.

    Args
    ----
    csv : str | Path
        Path to a comma-separated RGB colormap file.

    Returns
    -------
    None
        The colormap is registered with Matplotlib in place.
    """
    global CUSTOM_CMAPS
    import os
    import numpy as np
    import matplotlib as mpl

    cmap = os.path.splitext(os.path.basename(csv))[0]
    if cmap not in CUSTOM_CMAPS:
        CUSTOM_CMAPS.append(cmap)
    cmap_data = np.loadtxt(csv, delimiter=",")
    if cmap not in mpl.colormaps.keys():
        mpl_data = __RGBToPyCmap(cmap_data)
        mpl.colormaps.register(
            cmap=mcolors.LinearSegmentedColormap(cmap, mpl_data, cmap_data.shape[0])
        )
    cmap = f"{cmap}_r"
    if cmap not in mpl.colormaps.keys():
        mpl_data_r = __RGBToPyCmap(cmap_data[::-1, :])
        mpl.colormaps.register(
            cmap=mcolors.LinearSegmentedColormap(cmap, mpl_data_r, cmap_data.shape[0])
        )


def __ReadStyle(path):
    with warnings.catch_warnings(record=True):
        return rc_params_from_file(path, use_default_template=False)


def __RegisterStyles(styles_path):
    """Register bundled Matplotlib styles and composed style recipes."""
    styles = {}

    for path in sorted(Path(styles_path).glob("*.mplstyle")):
        styles[path.stem] = __ReadStyle(path)

    for style_name, recipe in _STYLE_RECIPES.items():
        composed = {}
        for part_name in recipe:
            try:
                composed.update(styles[part_name])
            except KeyError as exc:
                raise KeyError(
                    f"Style recipe {style_name!r} references missing part {part_name!r}"
                ) from exc

        styles[style_name] = composed

    plt.style.library.update(styles)
    plt.style.available[:] = sorted(
        name for name in plt.style.library if not name.startswith("_")
    )


def __RegisterColormaps(cmap_dir):
    """Register bundled CSV colormaps.

    Args
    ----
    cmap_dir : str | Path
        Directory containing CSV colormap files.

    Returns
    -------
    list[str]
        Names of colormap files found in `cmap_dir`.
    """
    cmap_paths = [path for path in sorted(Path(cmap_dir).iterdir()) if path.is_file()]
    for path in cmap_paths:
        __InstallCmapFromCSV(path)
    return [path.name for path in cmap_paths]


def __RegisterFonts(font_dir):
    """Register bundled font files.

    Args
    ----
    font_dir : str | Path
        Directory containing font files.

    Returns
    -------
    list[str]
        Font files found by Matplotlib and registered with its font manager.
    """
    font_files = font_manager.findSystemFonts(fontpaths=[str(font_dir)])
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)
    return font_files


def register():
    """Register bundled Matplotlib assets.

    Returns
    -------
    None
        Styles, colormaps, and fonts are registered with Matplotlib in place.
    """
    global CMAPS, font_files, _ASSETS_REGISTERED

    if _ASSETS_REGISTERED:
        return

    __RegisterStyles(styles_path)
    CMAPS = __RegisterColormaps(CMAP_DIR)
    font_files = __RegisterFonts(FONT_DIR)
    _ASSETS_REGISTERED = True


_quiet_matplotlib_warnings()
register()
