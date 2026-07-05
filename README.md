# `myplotlib`

`matplotlib` binder with custom styles and routines for fast plotting. see [previews of available styles](https://github.com/haykh/myplotlib/tree/master/previews#readme).

## installation

```shell
pip install myplotlib
```

## usage

### loading style, fonts & colormaps

```python
import matplotlib.pyplot as plt
from myplotlib import register

register()

plt.style.use(STYLE)
# STYLE can be:
# - fancy.dark, fancy.light
# - classic.dark, classic.light
# - mono.dark, mono.light
# - guttenberg.dark, guttenberg.light
# - soviet
# - latex

# you may also combine the styles:
plt.style.use([STYLE1, STYLE2])

# and you can temporarily load the style:
with plt.style.context(STYLE):
    plt.plot(...)
```

> `register()` loads the bundled styles, fonts, and colormaps into Matplotlib. importing `myplotlib` still registers them for backward compatibility, but the explicit call keeps linters from flagging an unused side-effect import.

### auxiliary plotting functions

```python
import myplotlib.plots as myplt
# type for docstring:
myplt?

# for specific function:
myplt.plot2d?

# preview custom styles with built-in functions
import myplotlib.tests as mypltest
# type for docstring:
mypltest?
```

the `guttenberg` styles mimic renaissance-era book illustrations: old-style lettering (P22 Operina Pro, with EB Garamond as fallback for missing glyphs), imperfect hand-drawn lines, and a single-ink line cycle. they pair well with `myplt.hatchedCircle`, which shades circles with engraving-style hatching (optionally only the crescent shadow, as on old drawings of moon phases):

```python
with plt.style.context("guttenberg.light"):
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    myplt.hatchedCircle(ax, (0, 0), 1, angle=45, spacing=0.15)
    myplt.hatchedCircle(ax, (2.5, 0), 1, shade_from=0, shade_depth=0.8)
```

for more usage examples checkout the `tests/` submodule.

## requirements

* `python >= 3.10`
* `latex` (used for `fancy` and `latex` only)

## To-do

- [ ] isocontour plotting
- [x] add streamplot for fieldline plotting
- [x] print all the newly added colormaps and the default color sequence
- [x] add a test plot for the demo
- [x] add image to readme
- [x] dark mode
- [x] monotype non-Latex mode
