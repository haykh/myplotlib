"""
`myplotlib.tests`

commands to help preview the custom styles (function names are self-descriptive). available functions are:

* testColormaps
* testColors
* testScatter
* testPlot
* testErrorbar
* testPlot2d
* testVectorPlot2d
* testHatching

* testAll
"""

import myplotlib.plots as myplt
import myplotlib

import matplotlib
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np


def __getAx(ax):
    if ax is None:
        fig, ax = plt.subplots()
    return ax


def testColormaps(ax=None):
    ax = __getAx(ax)
    zz = [np.linspace(0, 1, 256)]
    pad = 0.3
    dy = (1 - pad) / (len(myplotlib.CUSTOM_CMAPS))
    pady = pad / (len(myplotlib.CUSTOM_CMAPS))
    for i, cm in enumerate(myplotlib.CUSTOM_CMAPS):
        y1, y2 = (pady * (i + 0.5) + dy * i, pady * (i + 0.5) + dy * (i + 1))
        ax.imshow(zz, extent=(0, 1, y1, y2), cmap=cm)
        if matplotlib.rcParams["text.usetex"]:
            name = r"$\texttt{{`{}'}}$".format(cm)
        else:
            name = f"'{cm}'"
        ax.text(1.04, 0.5 * (y1 + y2), name, va="center", ha="left")
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("extra colormaps")


def testColors(ax=None):
    ax = __getAx(ax)
    prop_cycle = plt.rcParams["axes.prop_cycle"]
    colors = prop_cycle.by_key()["color"]
    title = "default color cycle"
    ax.set_title(title)
    for j, c in enumerate(colors):
        v_offset = -(j / len(colors))
        th = np.linspace(0, 2 * np.pi, 512)
        ax.plot(th, 0.1 * np.sin(th) + v_offset, color=c, lw=2)
        if matplotlib.rcParams["text.usetex"]:
            name = r"$\texttt{{'C{}'}}$".format(j)
        else:
            name = f"'C{j}'"
        ax.annotate(
            name,
            (0, v_offset),
            xytext=(-1.5, 0),
            ha="right",
            va="center",
            color=c,
            textcoords="offset points",
        )
        chex = mcolors.to_hex(c)
        if matplotlib.rcParams["text.usetex"]:
            name = r"$\texttt{{{}}}$".format(chex.replace("#", r"\#"))
        else:
            name = f"{chex}"
        ax.annotate(
            name,
            (2 * np.pi, v_offset),
            xytext=(1.5, 0),
            ha="left",
            va="center",
            color=c,
            textcoords="offset points",
        )
        ax.axis("off")


def testScatter(ax=None):
    ax = __getAx(ax)
    myplt.scatter(
        ax,
        np.random.random(100),
        np.random.random(100),
        xlog=True,
        ylog=True,
        s=(0.1 + np.random.random(100)) * 20,
        c="C0",
        label="drunk points",
        marker="*",
    )
    myplt.scatter(
        ax,
        10 ** (np.random.random(100) * 2),
        10 ** (np.random.random(100) * 2),
        xlog=True,
        ylog=True,
        s=(0.1 + np.random.random(100)) * 20,
        c="C1",
        label="sober points",
        ylim=(1e-2, None),
        xlim=(1e-2, None),
    )
    ax.legend(
        loc="lower left",
        bbox_to_anchor=(0, 1.0),
        borderaxespad=0.0,
        ncol=2,
        frameon=False,
    )
    ax.set_xlabel(r"some funny number $x^2/y$ [units]")
    ax.set_ylabel(r"other number $z_{\nu}$ [units]")


def testPlot(ax=None):
    ax = __getAx(ax)
    usetex = matplotlib.rcParams["text.usetex"]
    myplt.plot(
        ax,
        np.arange(100),
        20 * (2 + np.sin(np.linspace(0, 20, 100)) + np.random.random(100) ** 5),
        c="C4",
        ls=":",
        label="measurement #1" if not usetex else r"measurement \#1",
    )
    myplt.plot(
        ax,
        np.arange(100),
        20 * (2 + np.sin(np.linspace(0, 20, 100)) + np.random.random(100) ** 5),
        c="C2",
        label="measurement #2" if not usetex else r"measurement \#2",
    )
    ax.set_ylabel(r"probability [$\%$]")
    ax.set_xlabel("age [yr]")
    ax.set_ylim(0, 100)
    ax.legend(loc="upper center", frameon=False, ncol=2)


def testErrorbar(ax=None):
    ax = __getAx(ax)
    x = np.linspace(0, 1000, 10)
    y = np.sin(x / 100)
    dy = np.random.random(len(x)) * (y + 1.5) / 3
    myplt.dataPlot(
        ax.errorbar,
        ax,
        x,
        y,
        yerr=dy,
        marker="o",
        markeredgecolor=ax.get_facecolor(),
        markerfacecolor="C11",
        markeredgewidth=1.5,
    )
    ax.set_xlabel("time [s]")
    ax.set_ylabel("my very accurately measured variable [ly]")


def testPlot2d(ax=None):
    ax = __getAx(ax)
    x = np.linspace(-3, 3, 240)
    y = np.linspace(-3, 3, 200)
    xx, yy = np.meshgrid(x, y)
    zz = (xx**2 - np.sin(xx * yy**3)) + 6 * np.exp(-(xx**2 + yy**2) / 0.2)
    myplt.plot2d(ax, x, y, zz, cmap="bipolar", centering="edge")
    ax.set_xlabel("landscape in $x$")
    ax.set_ylabel("landscape in $y$")


def testVectorPlot2d(ax=None):
    ax = __getAx(ax)
    vortex_spacing = 0.5
    extra_factor = 2.0
    a = np.array([1, 0]) * vortex_spacing
    b = np.array([np.cos(np.pi / 3), np.sin(np.pi / 3)]) * vortex_spacing
    rnv = int(2 * extra_factor / vortex_spacing)
    vortices = [n * a + m * b for n in range(-rnv, rnv) for m in range(-rnv, rnv)]
    vortices = [
        (x, y)
        for (x, y) in vortices
        if -extra_factor < x < extra_factor and -extra_factor < y < extra_factor
    ]
    sx, sy = (1000, 1000)
    xs = np.linspace(-1, 1, sx).astype(np.float64)[None, :]
    ys = np.linspace(-1, 1, sy).astype(np.float64)[:, None]
    vectors = np.zeros((sx, sy, 2), dtype=np.float64)
    for x, y in vortices:
        rsq = (xs - x) ** 2 + (ys - y) ** 2
        vectors[..., 0] += (ys - y) / rsq
        vectors[..., 1] += -(xs - x) / rsq
    myplt.plotVectorField(
        ax,
        xs,
        ys,
        vectors[:, :, 0],
        vectors[:, :, 1],
        norm=mcolors.LogNorm(1, 1e2),
        cmap="turbo",
        lic_contrast=1,
    )


def testHatching(ax=None):
    ax = __getAx(ax)
    ax.set_aspect("equal")
    # fully hatched & crosshatched disks
    myplt.hatchedCircle(ax, (-1.5, 1.6), 1.0, angle=45, spacing=0.18)
    myplt.hatchedCircle(ax, (1.5, 1.6), 0.8, angle=30, spacing=0.22, crosshatch=True)
    # phases of venus: crescent shadows of decreasing depth
    for i, depth in enumerate([1.4, 1.0, 0.7, 0.4]):
        myplt.hatchedCircle(
            ax,
            (i * 1.7 - 2.55, -1.2),
            0.7,
            angle=75,
            spacing=0.15,
            shade_from=0.0,
            shade_depth=depth,
        )
    ax.set_title("hatched circles")
    ax.axis("off")


def testAll():
    fig = plt.figure(figsize=(8.5, 11), dpi=300, layout="constrained")
    gs = fig.add_gridspec(4, 2)
    axes = [fig.add_subplot(gs[i, j]) for i in range(4) for j in range(2)]

    test_plots = [
        testColors,
        testColormaps,
        testScatter,
        testPlot,
        testErrorbar,
        testPlot2d,
        testVectorPlot2d,
        testHatching,
    ]

    for ax, test_plot in zip(axes, test_plots):
        test_plot(ax)
