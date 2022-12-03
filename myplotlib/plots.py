"""
`myplotlib.plots`

a collection of handy plotting functions bound around `matplotlib` with lots of nice perks.

* dataPlot .................. : plot generic x & y 1d data (pass an `ax` method)
* scatter ................... : scatter plot (`dataPlot` with `ax.scatter`)
* plot ...................... : regular plot (`dataPlot` with `ax.plot`)
* plot2d .................... : 2d plot using `imshow`
* plotVectorField ........... : 2d plot with vector field

docstrings are available for all of the functions. type, e.g., `dataPlot?` to read about the arguments passed.
"""

import numpy as np


def __stretch(left, right, pad):
    c = 0.5 * (left + right)
    d = 0.5 * (right - left)
    return (c - d * pad, c + d * pad)


def __setMinMax(lims, data):
    if not lims:
        lims = (np.nanmin(data), np.nanmax(data))
    if lims[0] == None:
        lims = (np.nanmin(data), lims[1])
    if lims[1] == None:
        lims = (lims[0], np.nanmax(data))
    return lims


def __setAxLims(ax, coords, log, pad, lim, spines):
    lim = __setMinMax(lim, coords)
    # TODO: fix negative when log specified
    if pad > 0:
        ax.spines[spines].set_bounds(*lim)
    if spines == "bottom":
        func_setscale = ax.set_xscale
        func_setlim = ax.set_xlim
    elif spines == "left":
        func_setscale = ax.set_yscale
        func_setlim = ax.set_ylim
    else:
        raise ValueError
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


def __checkDimensions2d(x, y, zz):
    x, y, zz = (
        np.array(np.squeeze(x)),
        np.array(np.squeeze(y)),
        np.array(np.squeeze(zz)),
    )
    readShapes = f"`x.shape={x.shape}`, `y.shape={y.shape}`, `zz.shape={zz.shape}`"
    assert len(x.shape) == len(
        y.shape
    ), f"Shapes of `x` and `y` must be of the same dimension: {readShapes}."
    if len(x.shape) > 1:
        x = x[0, ...]
    if len(y.shape) > 1:
        y = y[..., 0]
    assert (len(zz.shape) == 2) or (
        len(zz.shape) == 3 and ((zz.shape[-1] == 3) or (zz.shape[-1] == 4))
    ), f"`zz` must have exactly 2 non-trivial axes: {readShapes}."
    assert (
        zz.shape[1] == x.shape[0]
    ), f"incompatible dimensions between `x` and `zz`: {readShapes}."
    assert (
        zz.shape[0] == y.shape[0]
    ), f"incompatible dimensions between `y` and `zz`: {readShapes}."
    return (x, y, zz)


def __findExtent(x, y, centering):
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
    function,
    ax,
    x,
    y,
    xlog=False,
    ylog=False,
    xlim=None,
    ylim=None,
    padx=0.0,
    pady=0.0,
    **kwargs,
):
    """
    add a plot according to a passed function

    args
    ----------
    function .................... : `ax.<METHOD>` used to make the plot (e.g. `ax.step`, `ax.errorbar`)
    ax .......................... : matplotlib axis object
    x, y ........................ : 1d data arrays
    xlog [False], ylog [False] .. : use log in x or y direction
    xlim [None], ylim [None] .... : tuples of x and y limits (None = determine from data)
    padx [0], pady [0] .......... : add whitespace to axes in each direction (0 = no additional space)
    **kwargs .................... : standard matplotlib kwargs passed to `ax.scatter`
    """
    if padx != 0:
        ax.spines["top"].set_visible(False)
    if pady != 0:
        ax.spines["right"].set_visible(False)
    function(x, y, **kwargs)
    __setAxLims(ax, x, xlog, padx, xlim, "bottom")
    __setAxLims(ax, y, ylog, pady, ylim, "left")
    return None


def scatter(
    ax, x, y, xlog=False, ylog=False, xlim=None, ylim=None, padx=0.0, pady=0.0, **kwargs
):
    """
    add a scatter plot to a given axis (same as `dataPlot(ax.scatter, ...)`)

    args
    ----------
    ax .......................... : matplotlib axis object
    x, y ........................ : 1d data arrays
    xlog [False], ylog [False] .. : use log in x or y direction
    xlim [None], ylim [None] .... : tuples of x and y limits (None = determine from data)
    padx [0], pady [0] .......... : add whitespace to axes in each direction (0 = no additional space)
    **kwargs .................... : standard matplotlib kwargs passed to `ax.scatter`
    """
    return dataPlot(ax.scatter, ax, x, y, xlog, ylog, xlim, ylim, padx, pady, **kwargs)


def plot(
    ax, x, y, xlog=False, ylog=False, xlim=None, ylim=None, padx=0.0, pady=0.0, **kwargs
):
    """
    add a simple plot to a given axis (same as `dataPlot(ax.plot, ...)`)

    args
    ----------
    ax .......................... : matplotlib axis object
    x, y ........................ : 1d data arrays
    xlog [False], ylog [False] .. : use log in x or y direction
    xlim [None], ylim [None] .... : tuples of x and y limits (None = determine from data)
    padx [0], pady [0] .......... : add whitespace to axes in each direction (0 = no additional space)
    **kwargs .................... : standard matplotlib kwargs passed to `ax.scatter`
    """
    dataPlot(ax.plot, ax, x, y, xlog, ylog, xlim, ylim, padx, pady, **kwargs)


def plot2d(
    ax,
    x,
    y,
    zz,
    force_aspect=True,
    centering="edge",
    xlim=None,
    ylim=None,
    zlog=False,
    zlim=None,
    padx=0.0,
    pady=0.0,
    cbar="5%",
    cbar_pad=0.05,
    **kwargs,
):
    """
    add a 2d plot to a given axis

    args
    ----------
    ax .......................... : matplotlib axis object
    x, y ........................ : 1d or 2d arrays of coordinates
    force_aspect [True] ......... : force equal aspect ratio according to axes
    centering ['edge'] .......... : centering of x & y nodes for the data ('edge', 'center')
    xlim [None], ylim [None] .... : tuples of x and y limits (None = determine from x & y)
    zlog [False] ................ : use log in z ('True', 'False')
    zlim [None] ................. : tuple of z limits (None = determine from z)
    padx [0], pady [0] .......... : add whitespace to axes in each direction (0 = no additional space)
    cbar ['5%'] ................. : size of the colorbar in percent of x-axis (None = no colorbar)
    cbar_pad [0.05] ............. : padding of the colorbar
    **kwargs .................... : standard matplotlib kwargs passed to `ax.scatter`

    returns
    ----------
    `None` ...................... : if `cbar` is `None`
    colorbar handle ............. : if `cbar` is not `None`
    """
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    import matplotlib.pyplot as plt
    import matplotlib as mpl

    x, y, zz = __checkDimensions2d(x, y, zz)
    ax.grid(False)
    extent = __findExtent(x, y, centering)
    aspect = "auto" if not force_aspect else None
    if not ("norm" in kwargs):
        if zlim is None:
            # vmin = np.nanmin(zz)
            # vmax = np.nanmax(zz)
            # print (vmin, vmax)
            # if (np.abs(vmin) > 0) and \
            #     (((np.abs(vmax / vmin) > 1e4) and not zlog) or\
            #     ((np.abs(vmax / vmin) > 1e6) and zlog)):
            vmax = np.quantile(zz[~np.isnan(zz)], 0.95)
            vmin = np.quantile(zz[~np.isnan(zz)], 0.05)
        else:
            vmin, vmax = zlim
        if zlog:
            if vmin < 0:
                vmin = vmax / 1e6
            norm = mpl.colors.LogNorm(vmin=vmin, vmax=vmax)
        else:
            norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    else:
        norm = kwargs.get("norm")
        kwargs.pop("norm")
    ax.imshow(zz, origin="lower", extent=extent, aspect=aspect, norm=norm, **kwargs)
    __setAxLims(ax, np.linspace(extent[0], extent[1]), False, padx, xlim, "bottom")
    __setAxLims(ax, np.linspace(extent[2], extent[3]), False, pady, ylim, "left")
    if cbar is not None:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size=cbar, pad=cbar_pad)
        colorbar = plt.colorbar(ax.get_images()[0], cax=cax)
        return colorbar
    else:
        return None


def plotVectorField(
    ax,
    x,
    y,
    fx,
    fy,
    background=None,
    texture_seed=None,
    kernel_len=31,
    kernel_pow=1,
    lic_alphamin=0.5,
    lic_alphamax=0.75,
    lic_contrast=0.33,
    lic_opacity=0.75,
    lic_cmap="binary_r",
    force_aspect=True,
    centering="edge",
    xlim=None,
    ylim=None,
    padx=0.0,
    pady=0.0,
    cbar="5%",
    cbar_pad=0.05,
    **kwargs,
):
    """
    add a 2d plot with a vector-field overplotted

    args
    ----------
    ax .......................... : matplotlib axis object
    x, y ........................ : 1d or 2d arrays of coordinates
    fx, fy ...................... : 2d arrays of the vector field components
    background [None] ........... : 2d array of the image background (None = `sqrt(fx^2 + fy^2)`)

    line integral convolution (lic) parameters
    ----------
    texture_seed [None] ......... : specify a random seed to generate textures, useful when rendering movies (None = random)
    kernel_len [31] ............. : kernel resolution for the lic algorithm
    kernel_pow [1] .............. : kernel sharpness for the lic algorithm
    lic_alphamin [0.5] .......... : lic parameter for min transparency
    lic_alphamax [0.75] ......... : lic parameter for max transparency
    lic_contrast [0.33] ......... : lic parameter for the contrast
    lic_opacity [0.75] .......... : lic parameter for the absolute opacity of the field plot
    lic_cmap ['binary_r'] ....... : colormap used for the lic texture

    the rest of the args are the same as for the `plot2d`
    ----------
    force_aspect [True] ......... : force equal aspect ratio according to axes
    centering ['edge'] .......... : centering of x & y nodes for the data ('edge', 'center')
    xlim [None], ylim [None] .... : tuples of x and y limits (None = determine from x & y)
    padx [0], pady [0] .......... : add whitespace to axes in each direction (0 = no additional space)
    cbar ['5%'] ................. : size of the colorbar in percent of x-axis (None = no colorbar)
    cbar_pad [0.05] ............. : padding of the colorbar
    **kwargs .................... : standard matplotlib kwargs passed to `ax.scatter`
    """
    import myplotlib.tools.lic as lic
    import matplotlib
    import matplotlib.pyplot as plt

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
    alphas = matplotlib.colors.Normalize(None, None, clip=True)(_)
    alphas[alphas < lic_alphamin] = 0
    alphas[alphas > lic_alphamax] = 1
    _ = (
        np.sign(weights - np.average(weights))
        * np.abs(weights - np.average(weights)) ** lic_contrast
    )
    colors = matplotlib.colors.Normalize(None, None)(_)
    colors = plt.cm.get_cmap(lic_cmap)(colors)
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
        cbar=cbar,
        cbar_pad=cbar_pad,
        alpha=lic_opacity,
    )
    return colorbar
