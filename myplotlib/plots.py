"""Convenience plotting helpers built around `matplotlib`.

Functions
---------
dataPlot
    Plot generic x and y data with a passed axis method.
scatter
    Add a scatter plot with shared limit/log handling.
plot
    Add a line plot with shared limit/log handling.
plot2d
    Add a 2D image plot with optional colorbar handling.
plotVectorField
    Add a 2D image plot with a line-integral-convolution vector overlay.
hatchedCircle
    Draw a circle shaded with engraving-style hatching.
plot2dGrid
    Add a grid of 2D plots with shared axes.
"""

from typing import TypeAlias, Any, TypedDict, Callable, Union, Tuple
import numpy as np
from numpy.typing import NDArray
import matplotlib.colors as mcolors
from matplotlib.axes._axes import Axes as pltAxes

LimTypeWithNone: TypeAlias = Union[Tuple[Union[float, None], Union[float, None]], None]
LimType: TypeAlias = Tuple[float, float]


def __stretch(
    left: float,
    right: float,
    pad: float,
) -> LimType:
    """Stretch limits around their midpoint by a padding factor.

    Args
    ----
    left : float
        The lower limit.
    right : float
        The upper limit.
    pad : float
        Multiplicative padding factor applied to the half-width.

    Returns
    -------
    tuple[float, float]
        The stretched lower and upper limits.
    """
    c = 0.5 * (left + right)
    d = 0.5 * (right - left)
    return (c - d * pad, c + d * pad)


def __setMinMax(
    lims: LimTypeWithNone,
    data: Union[NDArray, list],
) -> LimType:
    """Resolve axis limits from optional bounds and data.

    Args
    ----
    lims : tuple[float | None, float | None] | None
        Explicit lower and upper limits; `None` values are inferred from data.
    data : NDArray | list
        Data used to infer missing limits.

    Returns
    -------
    tuple[float, float]
        The resolved lower and upper limits.

    Raises
    ------
    TypeError
        If `lims` is not a tuple or `None`.
    ValueError
        If `lims` is not a tuple of length 2, or if it contains `None` values
        when both limits are specified.
    """
    if lims is None:
        return (np.nanmin(data), np.nanmax(data))
    if not isinstance(lims, tuple):
        raise TypeError("lims must be a tuple of length 2 or None")
    elif len(lims) != 2:
        raise ValueError("lims must be a tuple of length 2")
    if lims[0] is None and lims[1] is None:
        return (np.nanmin(data), np.nanmax(data))
    if lims[0] is None and lims[1] is not None:
        return (np.nanmin(data), lims[1])
    if lims[1] is None and lims[0] is not None:
        return (lims[0], np.nanmax(data))
    if lims[0] is None or lims[1] is None:
        raise ValueError("lims must not contain None values")
    return (lims[0], lims[1])


def __setAxLims(
    ax: pltAxes,
    coords: Union[NDArray, list],
    log: bool,
    pad: float,
    lims: LimTypeWithNone,
    spines: str,
):
    """Set axis limits and scale from data, padding, and explicit bounds.

    Args
    ----
    ax : pltAxes
        The matplotlib axis object.
    coords : NDArray | list
        Coordinate values used to infer missing limits.
    log : bool
        Use logarithmic scaling for the selected axis.
    pad : float
        Fractional padding applied around the resolved limits.
    lims : tuple[float | None, float | None] | None
        Explicit axis limits; `None` values are inferred from `coords`.
    spines : str
        Axis spine to configure (`'bottom'` for x, `'left'` for y).

    Raises
    ------
    ValueError
        If `spines` is neither `'bottom'` nor `'left'`.
    """
    if log and (
        lims is None or (isinstance(lims, tuple) and len(lims) == 2 and None in lims)
    ):
        coords = np.asarray(coords)
        coords = coords[coords > 0]
        if coords.size == 0:
            raise ValueError("log scale requires positive coordinate values")
    lim = __setMinMax(lims, coords)
    if log and (lim[0] <= 0 or lim[1] <= 0):
        raise ValueError("log scale requires positive axis limits")
    if pad > 0:
        ax.spines[spines].set_bounds(*lim)
    if spines == "bottom":
        func_setscale = ax.set_xscale
        func_setlim = ax.set_xlim
    elif spines == "left":
        func_setscale = ax.set_yscale
        func_setlim = ax.set_ylim
    else:
        raise ValueError(f"invalid `spines` value: {spines}")
    if log:
        func_setscale("log")
        p1, p2 = lim
        func_setlim(
            *list(
                map(lambda p: 10**p, __stretch(np.log10(p1), np.log10(p2), 1.0 + pad))
            )
        )
    else:
        p1, p2 = lim
        func_setlim(*__stretch(p1, p2, 1.0 + pad))


def __checkDimensions2d(
    x: NDArray,
    y: NDArray,
    zz: NDArray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Validate 2D field dimensions and return squeezed arrays.

    Args
    ----
    x, y : NDArray
        1D or 2D coordinate arrays.
    zz : NDArray
        2D scalar field or 3D RGB/RGBA image array.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray]
        Squeezed `x`, `y`, and `zz` arrays with compatible dimensions.

    Raises
    ------
    ValueError
        If the coordinate and field shapes are incompatible.
    """
    x, y, zz = (
        np.array(np.squeeze(x)),
        np.array(np.squeeze(y)),
        np.array(np.squeeze(zz)),
    )
    readShapes = f"`x.shape={x.shape}`, `y.shape={y.shape}`, `zz.shape={zz.shape}`"
    if len(x.shape) != len(y.shape):
        raise ValueError(
            f"Shapes of `x` and `y` must be of the same dimension: {readShapes}."
        )
    if len(x.shape) > 1:
        x = x[0, ...]
    if len(y.shape) > 1:
        y = y[..., 0]
    if len(zz.shape) != 2 and (
        len(zz.shape) != 3 or ((zz.shape[-1] != 3) and (zz.shape[-1] != 4))
    ):
        raise ValueError(f"`zz` must have exactly 2 non-trivial axes: {readShapes}.")

    if zz.shape[1] != x.size:
        raise ValueError(f"incompatible dimensions between `x` and `zz`: {readShapes}.")
    if zz.shape[0] != y.size:
        raise ValueError(f"incompatible dimensions between `y` and `zz`: {readShapes}.")
    return (x, y, zz)


def __findExtent(
    x: NDArray,
    y: NDArray,
    centering: str,
) -> tuple[float, float, float, float]:
    """Find the `imshow` extent for edge- or center-located samples.

    Args
    ----
    x, y : NDArray
        1D coordinate arrays.
    centering : str
        Coordinate convention (`'edge'` or `'center'`).

    Returns
    -------
    tuple[float, float, float, float]
        The image extent as `(left, right, bottom, top)`.

    Raises
    ------
    ValueError
        If `centering` is neither `'edge'` nor `'center'`.
    """
    if centering == "edge":
        dx = x[1] - x[0]
        dy = y[1] - y[0]
        extent = (x.min(), x.max() + dx, y.min(), y.max() + dy)
    elif centering == "center":
        dx = x[1] - x[0]
        dy = y[1] - y[0]
        extent = (
            x.min() - dx * 0.5,
            x.max() + dx * 0.5,
            y.min() - dy * 0.5,
            y.max() + dy * 0.5,
        )
    else:
        raise ValueError
    return extent


def dataPlot(
    function: Callable,
    ax: pltAxes,
    x: NDArray,
    y: NDArray,
    xlog: bool = False,
    ylog: bool = False,
    xlim: LimTypeWithNone = None,
    ylim: LimTypeWithNone = None,
    padx: float = 0.0,
    pady: float = 0.0,
    **kwargs,
):
    """Add a plot according to a passed function

    Args
    ----
    function : Callable
        The function to call on the axis (e.g., `ax.plot`, `ax.scatter`).
    ax : pltAxes
        The matplotlib axis object.
    x, y : NDArray
        The data to plot.
    xlog : bool, optional
        Use logarithmic scale for x-axis (default is False).
    ylog : bool, optional
        Use logarithmic scale for y-axis (default is False).
    xlim : tuple[float | None, float | None] | None, optional
        Tuple of x limits (None = determine from data) (default is None).
    ylim : tuple[float | None, float | None] | None, optional
        Tuple of y limits (None = determine from data) (default is None).
    padx : float, optional
        Add whitespace to axes in each direction (0 = no additional space) (default is 0.0).
    pady : float, optional
        Add whitespace to axes in each direction (0 = no additional space) (default is 0.0).
    **kwargs : dict, optional
        Standard matplotlib kwargs passed to `function`.

    Returns
    -------
    Any
        The artist or handle returned by `function`.
    """
    if padx != 0:
        ax.spines["top"].set_visible(False)
    if pady != 0:
        ax.spines["right"].set_visible(False)
    handle = function(x, y, **kwargs)
    __setAxLims(ax, x, xlog, padx, xlim, "bottom")
    __setAxLims(ax, y, ylog, pady, ylim, "left")
    return handle


def scatter(
    ax: pltAxes,
    x: NDArray,
    y: NDArray,
    xlog: bool = False,
    ylog: bool = False,
    xlim: LimTypeWithNone = None,
    ylim: LimTypeWithNone = None,
    padx: float = 0.0,
    pady: float = 0.0,
    **kwargs,
):
    """Add a scatter plot to a given axis

    Args
    ----
    ax : pltAxes
        The matplotlib axis object.
    x, y : NDArray
        The data to plot.
    xlog : bool, optional
        Use logarithmic scale for x-axis (default is False).
    ylog : bool, optional
        Use logarithmic scale for y-axis (default is False).
    xlim : LimTypeWithNone, optional
        Tuple of x limits (None = determine from data) (default is None).
    ylim : LimTypeWithNone, optional
        Tuple of y limits (None = determine from data) (default is None).
    padx : float, optional
        Add whitespace to axes in each direction (0 = no additional space) (default is 0.0).
    pady : float, optional
        Add whitespace to axes in each direction (0 = no additional space) (default is 0.0).
    **kwargs : dict, optional
        Standard matplotlib kwargs passed to `ax.scatter`.

    Returns
    -------
    PathCollection
        The collection returned by `ax.scatter`.
    """
    return dataPlot(ax.scatter, ax, x, y, xlog, ylog, xlim, ylim, padx, pady, **kwargs)


def plot(
    ax: pltAxes,
    x: NDArray,
    y: NDArray,
    xlog: bool = False,
    ylog: bool = False,
    xlim: LimTypeWithNone = None,
    ylim: LimTypeWithNone = None,
    padx: float = 0.0,
    pady: float = 0.0,
    **kwargs,
):
    """Add a plot to a given axis (same as `dataPlot(ax.plot, ...)`)

    Args
    ----
    ax : pltAxes
        The matplotlib axis object.
    x, y : NDArray
        The data to plot.
    xlog : bool, optional
        Use logarithmic scale for x-axis (default is False).
    ylog : bool, optional
        Use logarithmic scale for y-axis (default is False).
    xlim : LimTypeWithNone, optional
        Tuple of x limits (None = determine from data) (default is None).
    ylim : LimTypeWithNone, optional
        Tuple of y limits (None = determine from data) (default is None).
    padx : float, optional
        Add whitespace to axes in each direction (0 = no additional space) (default is 0.0).
    pady : float, optional
        Add whitespace to axes in each direction (0 = no additional space) (default is 0.0).
    **kwargs : dict, optional
        Standard matplotlib kwargs passed to `ax.plot`.

    Returns
    -------
    list[Line2D]
        The line artists returned by `ax.plot`.
    """
    return dataPlot(ax.plot, ax, x, y, xlog, ylog, xlim, ylim, padx, pady, **kwargs)


def plot2d(
    ax: pltAxes,
    x: NDArray,
    y: NDArray,
    zz: NDArray,
    force_aspect: bool = True,
    centering: str = "edge",
    xlim: LimTypeWithNone = None,
    ylim: LimTypeWithNone = None,
    zlog: bool = False,
    zlim: LimTypeWithNone = None,
    padx: float = 0.0,
    pady: float = 0.0,
    cbar: Union[str, None] = "5%",
    cbar_pad: float = 0.05,
    cbar_pos: str = "right",
    **kwargs,
):
    """Add a 2d plot to a given axis

    Args
    ----
    ax : pltAxes
        The matplotlib axis object.
    x, y : NDArray
        The coordinates of the data to plot.
    zz : NDArray
        2D scalar field or 3D RGB/RGBA image array.
    force_aspect : bool, optional
        Force equal aspect ratio according to axes (default is True).
    centering : str, optional
        Centering of x & y nodes for the data ('edge', 'center') (default is 'edge').
    xlim : tuple[float | None, float | None] | None, optional
        Tuple of x limits (None = determine from x) (default is None).
    ylim : tuple[float | None, float | None] | None, optional
        Tuple of y limits (None = determine from y) (default is None).
    zlog : bool, optional
        Use log in z ('True', 'False') (default is False).
    zlim : tuple[float | None, float | None] | None, optional
        Tuple of z limits (None = determine from z) (default is None).
    padx : float, optional
        Add whitespace to axes in each direction (0 = no additional space) (default is 0.0).
    pady : float, optional
        Add whitespace to axes in each direction (0 = no additional space) (default is 0.0).
    cbar : str | None, optional
        Size of the colorbar in percent of x-axis (None = no colorbar) (default is '5%').
    cbar_pad : float, optional
        Padding of the colorbar (default is 0.05).
    cbar_pos : str, optional
        Position of the colorbar ('left', 'right', 'top', 'bottom') (default is 'right').
    **kwargs : dict, optional
        Standard matplotlib kwargs passed to `ax.imshow`.

    Returns
    -------
    Colorbar | None
        Returns `None` if `cbar` is `None`, otherwise returns the colorbar handle.

    Raises
    ------
    ValueError
        If `centering` is not 'edge' or 'center', or if `cbar_pos` is not one of 'left', 'right', 'top', or 'bottom'.
    """
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    import matplotlib.pyplot as plt

    if centering not in ["edge", "center"]:
        raise ValueError("invalid `centering` value: must be 'edge' or 'center'")
    if cbar_pos not in ["left", "right", "top", "bottom"]:
        raise ValueError(
            "invalid `cbar_pos` value: must be 'left', 'right', 'top', or 'bottom'"
        )

    x, y, zz = __checkDimensions2d(x, y, zz)
    ax.grid(False)
    extent = __findExtent(x, y, centering)
    aspect = "auto" if not force_aspect else None
    if "norm" not in kwargs:
        zminQ = np.quantile(zz[~np.isnan(zz) & ~np.isinf(zz)], 0.05)
        zmaxQ = np.quantile(zz[~np.isnan(zz) & ~np.isinf(zz)], 0.95)
        if zlim is not None:
            if zlim[0] is None:
                vmin = zminQ
            else:
                vmin = zlim[0]
            if zlim[1] is None:
                vmax = zmaxQ
            else:
                vmax = zlim[1]
        else:
            vmin, vmax = zminQ, zmaxQ
        if zlog:
            norm = mcolors.LogNorm(vmin=float(vmin), vmax=float(vmax))
        else:
            norm = mcolors.Normalize(vmin=float(vmin), vmax=float(vmax))
    else:
        norm = kwargs.get("norm")
        kwargs.pop("norm")
    ax.imshow(zz, origin="lower", extent=extent, aspect=aspect, norm=norm, **kwargs)
    __setAxLims(ax, np.linspace(extent[0], extent[1]), False, padx, xlim, "bottom")
    __setAxLims(ax, np.linspace(extent[2], extent[3]), False, pady, ylim, "left")
    if cbar is not None:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes(cbar_pos, size=cbar, pad=cbar_pad)
        colorbar = plt.colorbar(
            ax.get_images()[0],
            cax=cax,
            orientation="vertical" if cbar_pos in ["left", "right"] else "horizontal",
        )
        if cbar_pos == "left":
            cax.yaxis.set_ticks_position("left")
            cax.yaxis.set_label_position("left")
            ax.yaxis.set_ticks_position("right")
            ax.yaxis.set_label_position("right")
        if cbar_pos == "top":
            cax.xaxis.set_ticks_position("top")
            cax.xaxis.set_label_position("top")
        if cbar_pos == "bottom":
            ax.xaxis.set_ticks_position("top")
            ax.xaxis.set_label_position("top")
        return colorbar
    else:
        return None


def plotVectorField(
    ax: pltAxes,
    x: NDArray,
    y: NDArray,
    fx: NDArray,
    fy: NDArray,
    background: Union[NDArray, None] = None,
    texture_seed: Union[int, None] = None,
    kernel_len: int = 31,
    kernel_pow: int = 1,
    lic_alphamin: float = 0.5,
    lic_alphamax: float = 0.75,
    lic_contrast: float = 0.33,
    lic_opacity: float = 0.75,
    lic_cmap: str = "binary_r",
    force_aspect: bool = True,
    centering: str = "edge",
    xlim: Union[Tuple[float, float], None] = None,
    ylim: Union[Tuple[float, float], None] = None,
    padx: float = 0.0,
    pady: float = 0.0,
    cbar: Union[str, None] = "5%",
    cbar_pad: float = 0.05,
    **kwargs,
):
    """Add a 2D plot with a vector-field overlay.

    Uses line integral convolution (LIC) to render the vector field as a
    semi-transparent texture on top of a scalar image background.

    Args
    ----
    ax : pltAxes
        The matplotlib axis object.
    x, y : NDArray
        1D or 2D arrays of coordinates.
    fx, fy : NDArray
        2D arrays of the vector field components.
    background : NDArray | None, optional
        2D array of the image background (None = `sqrt(fx^2 + fy^2)`).
    texture_seed : int | None, optional
        Specify a random seed to generate textures, useful when rendering movies (None = random).
    kernel_len : int, optional
        Kernel resolution for the LIC algorithm (default is 31).
    kernel_pow : int, optional
        Kernel sharpness for the LIC algorithm (default is 1).
    lic_alphamin : float, optional
        LIC parameter for minimum visible alpha (default is 0.5).
    lic_alphamax : float, optional
        LIC parameter for fully opaque alpha (default is 0.75).
    lic_contrast : float, optional
        LIC texture contrast exponent (default is 0.33).
    lic_opacity : float, optional
        Overall opacity of the LIC overlay (default is 0.75).
    lic_cmap : str, optional
        Colormap used for the LIC texture (default is 'binary_r').
    force_aspect : bool, optional
        Force equal aspect ratio according to axes (default is True).
    centering : str, optional
        Centering of x & y nodes for the data ('edge', 'center') (default is 'edge').
    xlim : tuple[float, float] | None, optional
        Tuple of x limits (None = determine from x) (default is None).
    ylim : tuple[float, float] | None, optional
        Tuple of y limits (None = determine from y) (default is None).
    padx : float, optional
        Add whitespace to axes in each direction (0 = no additional space) (default is 0.0).
    pady : float, optional
        Add whitespace to axes in each direction (0 = no additional space) (default is 0.0).
    cbar : str | None, optional
        Size of the colorbar in percent of x-axis (None = no colorbar) (default is '5%').
    cbar_pad : float, optional
        Padding of the colorbar (default is 0.05).
    **kwargs : dict, optional
        Standard matplotlib kwargs passed to the background `ax.imshow`.

    Returns
    -------
    Colorbar | None
        Returns `None` if `cbar` is `None`, otherwise returns the background colorbar handle.
    """
    import myplotlib.tools.lic as lic
    import matplotlib

    kernel = lic.generate_kernel(kernel_len) ** kernel_pow
    x, y, fx = __checkDimensions2d(x, y, fx)
    x, y, fy = __checkDimensions2d(x, y, fy)
    if background is None:
        background = np.sqrt(fx**2 + fy**2)
    # line integral convolution doesn't like zeros
    fmin = (np.abs(fx).min() + np.abs(fy).min()) / 1e10
    fx = (1.0 * (fx >= 0) - 1.0 * (fx < 0)) * (np.abs(fx) + fmin)
    fy = (1.0 * (fy >= 0) - 1.0 * (fy < 0)) * (np.abs(fy) + fmin)

    x, y, background = __checkDimensions2d(x, y, background)
    texture = lic.generate_texture(background.shape, texture_seed)
    img1 = lic.line_integral_convolution(fx, fy, texture, kernel)
    img2 = lic.line_integral_convolution(-fx, -fy, texture, kernel)
    img = 0.5 * (img1 + img2)

    weights = img
    _ = np.sign(weights - np.average(weights)) * np.sqrt(
        np.abs(weights - np.average(weights))
    )
    alphas = mcolors.Normalize(None, None, clip=True)(_)
    alphas[alphas < lic_alphamin] = 0
    alphas[alphas > lic_alphamax] = 1
    _ = (
        np.sign(weights - np.average(weights))
        * np.abs(weights - np.average(weights)) ** lic_contrast
    )
    colors = mcolors.Normalize(None, None)(_)
    colors = matplotlib.colormaps[lic_cmap](colors)
    colors[..., -1] = alphas

    colorbar = plot2d(
        ax,
        x,
        y,
        background,
        force_aspect=force_aspect,
        centering=centering,
        xlim=xlim,
        ylim=ylim,
        padx=padx,
        pady=pady,
        cbar=cbar,
        cbar_pad=cbar_pad,
        **kwargs,
    )
    plot2d(
        ax,
        x,
        y,
        colors,
        force_aspect=force_aspect,
        centering=centering,
        xlim=xlim,
        ylim=ylim,
        padx=padx,
        pady=pady,
        cbar=None,
        alpha=lic_opacity,
    )
    return colorbar


def hatchedCircle(
    ax: pltAxes,
    center: Tuple[float, float],
    radius: float,
    angle: float = 45.0,
    spacing: float = 0.12,
    shade_from: Union[float, None] = None,
    shade_depth: float = 0.75,
    crosshatch: bool = False,
    edge: bool = True,
    color: Union[str, Tuple[float, float, float, float], None] = None,
    linewidth: Union[float, None] = None,
    **kwargs,
):
    """Draw a circle shaded with engraving-style hatching

    Mimics the hatched shading of renaissance-era book illustrations
    (best combined with the `guttenberg` style, which makes the strokes
    imperfect via `path.sketch`). By default the whole disk is hatched;
    passing `shade_from` hatches only the crescent-shaped shadow opposite
    the light, as on woodcut drawings of moon phases.

    Args
    ----
    ax : pltAxes
        The matplotlib axis object (use `ax.set_aspect('equal')` to keep the circle round).
    center : tuple[float, float]
        The center of the circle in data coordinates.
    radius : float
        The radius of the circle in data coordinates.
    angle : float, optional
        Angle of the hatch lines in degrees (default is 45).
    spacing : float, optional
        Distance between hatch lines as a fraction of the radius (default is 0.12).
    shade_from : float | None, optional
        Direction the light comes from, in degrees (None = hatch the full disk) (default is None).
    shade_depth : float, optional
        How deep the shadow crescent cuts into the disk, from 0 (no shadow)
        to 2 (full disk); only used with `shade_from` (default is 0.75).
    crosshatch : bool, optional
        Add a second family of hatch lines perpendicular to the first (default is False).
    edge : bool, optional
        Draw the circle outline (default is True).
    color : str | tuple[float, float, float, float] | None, optional
        Ink color for the hatching and the outline (None = default line color) (default is None).
    linewidth : float | None, optional
        Width of the hatch lines and the outline (None = default line width) (default is None).
    **kwargs : dict, optional
        Standard matplotlib kwargs passed to the hatch `LineCollection`.

    Returns
    -------
    tuple[Circle | None, LineCollection]
        The outline patch (None if `edge=False`) and the hatch line collection.
    """
    import matplotlib as mpl
    from matplotlib.collections import LineCollection
    from matplotlib.patches import Circle

    if color is None:
        color = mcolors.to_rgba(mpl.rcParams["lines.color"])
    if linewidth is None:
        linewidth = mpl.rcParams["lines.linewidth"]

    c = np.asarray(center, dtype=float)
    angles = [angle, angle + 90.0] if crosshatch else [angle]
    if shade_from is not None:
        phi = np.deg2rad(shade_from)
        lit_center = c + shade_depth * radius * np.array([np.cos(phi), np.sin(phi)])

    segments = []
    for ang in angles:
        theta = np.deg2rad(ang)
        along = np.array([np.cos(theta), np.sin(theta)])
        normal = np.array([-np.sin(theta), np.cos(theta)])
        step = spacing * radius
        for s in np.arange(-radius + 0.5 * step, radius, step):
            half = np.sqrt(radius**2 - s**2)
            p0 = c + s * normal
            intervals = [(-half, half)]
            if shade_from is not None:
                # cut out the chord overlap with the lit circle (same radius,
                # displaced towards the light); what remains is the shadow
                m = p0 - lit_center
                b = np.dot(m, along)
                disc = b**2 - (np.dot(m, m) - radius**2)
                if disc > 0:
                    t1, t2 = -b - np.sqrt(disc), -b + np.sqrt(disc)
                    intervals = [
                        (a1, a2)
                        for a1, a2 in [(-half, min(t1, half)), (max(t2, -half), half)]
                        if a2 > a1
                    ]
            for a1, a2 in intervals:
                if a2 - a1 > 1e-3 * radius:
                    segments.append([p0 + a1 * along, p0 + a2 * along])

    hatches = LineCollection(
        segments, colors=color, linewidths=linewidth, capstyle="round", **kwargs
    )
    ax.add_collection(hatches)
    outline = None
    if edge:
        outline = Circle(
            tuple(c), radius, facecolor="none", edgecolor=color, linewidth=linewidth
        )
        ax.add_patch(outline)
    ax.update_datalim([c - radius, c + radius])
    ax.autoscale_view()
    return (outline, hatches)


class PanelDict(TypedDict):
    """Describe one panel in a `plot2dGrid` layout.

    Attributes
    ----------
    label : str | None
        Label for the panel.
    field : Callable | None
        Function that accepts the `fields` dictionary and returns the plotted array.
    cmap : str | None
        Colormap for the panel.
    norm : matplotlib.colors.Normalize | None
        Normalization object for the panel.
    """

    label: Union[str, None]
    field: Union[Callable, None]
    cmap: Union[str, None]
    norm: Union[mcolors.Normalize, None]


def plot2dGrid(
    x: NDArray,
    y: NDArray,
    fields: dict[str, np.ndarray],
    panels: list[list[PanelDict]],
    label_pos: str = "title",
    label_args: Union[dict[str, Any], None] = None,
    width: float = 10,
    dpi: int = 150,
    wspace: float = 0.05,
    hspace: float = 0.05,
    **kwargs,
):
    """Add a grid of 2D plots with shared axes.

    Args
    ----
    x, y : NDArray
        1D or 2D coordinate arrays.
    fields : dict[str, np.ndarray]
        Dictionary of all available fields.
    panels : list[list[PanelDict]]
        Rectangular grid of panel dictionaries. Each panel supplies a `field`
        callable and optional `label`, `cmap`, and `norm` values.
    label_pos : str, optional
        Position of the label ('title', 'cbar', 'text', None) (default is 'title').
    label_args : dict[str, Any] | None, optional
        Arguments passed to `ax.set_title`, `cbar.set_label`, or `ax.text`
        (None = use no extra label args) (default is None).
        For `label_pos='text'`, a `position` entry sets axes-relative text coordinates.
    width : float, optional
        Width of the figure in inches (default is 10).
    dpi : int, optional
        Figure resolution in dots per inch (default is 150).
    wspace : float, optional
        Width space between panels as a fraction of panel width (default is 0.05).
    hspace : float, optional
        Height space between panels as a fraction of panel height (default is 0.05).
    **kwargs : dict, optional
        Standard `plot2d` kwargs such as `force_aspect`, `centering`, `xlim`,
        `ylim`, `padx`, `pady`, `cbar`, and `cbar_pad`.

    Returns
    -------
    tuple[Figure, list[list[pltAxes]]]
        The created figure and nested list of axes.

    Raises
    ------
    ValueError
        If `panels` is empty, non-rectangular, missing required keys, or has an
        invalid `label_pos`.
    """
    import matplotlib.pyplot as plt

    if len(panels) == 0:
        raise ValueError("no panels to plot")
    if len(panels[0]) == 0:
        raise ValueError("no panels to plot")
    if not all([len(row) == len(panels[0]) for row in panels]):
        raise ValueError("all rows must have the same number of panels")
    if label_pos not in ["title", "cbar", "text", None]:
        raise ValueError("invalid label position")

    label_args = {} if label_args is None else dict(label_args)

    ncols = len(panels[0])
    nrows = len(panels)

    xlims = kwargs.get("xlim", (x.min(), x.max()))
    ylims = kwargs.get("ylim", (y.min(), y.max()))
    aspect = (xlims[1] - xlims[0]) / (ylims[1] - ylims[0])
    height = (
        width
        * ((nrows + hspace * (nrows - 1)) / (ncols + wspace * (ncols - 1)))
        / aspect
    )

    fig = plt.figure(figsize=(width, height), dpi=dpi)

    gs = fig.add_gridspec(nrows, ncols, wspace=wspace, hspace=hspace)
    axs = [[fig.add_subplot(gs[i, j]) for j in range(ncols)] for i in range(nrows)]

    label_coords = label_args.pop("position", (0.05, 0.95))

    for i in range(nrows):
        for j in range(ncols):
            ax = axs[i][j]
            panel = panels[i][j]
            if "field" not in panel:
                raise ValueError("panel must have a 'field' key")
            field_func = panel["field"]
            if field_func is None:
                raise ValueError("field must be a callable function")
            if not callable(field_func):
                raise TypeError("field must be a callable function")
            cbar = plot2d(
                ax,
                x,
                y,
                field_func(fields),
                norm=panel.get("norm"),
                cmap=panel.get("cmap"),
                **kwargs,
            )

            if j != 0:
                ax.set(ylabel=None, yticklabels=[])
            if i != nrows - 1:
                ax.set(xlabel=None, xticklabels=[])

            if label_pos == "title":
                if "label" not in panel:
                    raise ValueError("panel must have a 'label' key")
                if panel["label"] is not None:
                    ax.set_title(panel["label"], **label_args)
            elif label_pos == "cbar":
                if cbar is not None:
                    if "label" not in panel:
                        raise ValueError("panel must have a 'label' key")
                    if panel["label"] is not None:
                        cbar.set_label(panel["label"], **label_args)
            elif label_pos == "text":
                if "label" not in panel:
                    raise ValueError("panel must have a 'label' key")
                if panel["label"] is not None:
                    ax.text(
                        *label_coords,
                        s=panel["label"],
                        transform=ax.transAxes,
                        **label_args,
                    )

    return (fig, axs)
