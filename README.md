# `myplotlib`

`matplotlib` binder with custom styles and routines for fast plotting. see [previews of available styles](https://github.com/haykh/myplotlib/tree/master/previews#readme).

## installation

```shell
pip install myplotlib
```

## usage

### loading style, fonts & colormaps

```python
import myplotlib
import matplotlib.pyplot as plt

plt.style.use(STYLE)
# STYLE can be:
# - fancy.dark, fancy.light
# - classic.dark, classic.light
# - mono.dark, mono.light
# - latex

# you may also combine the styles:
plt.style.use([STYLE1, STYLE2])

# and you can temporarily load the style:
with plt.style.context(STYLE):
    plt.plot(...)
```

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

for more usage examples checkout the `tests/` submodule.

## requirements

* `python >= 3.8`
* `matplotlib >= 3.5.0`, `numpy`
* `latex` (used for `fancy` and `latex` only)
* `numba>=0.57.0`

## development

when deploying a new version, there are three necessary steps to take.

1. increase the version string in `myplotlib/__init__.py`.
2. generate the previews:
    ```sh
    python3 previews/export_previews.py
    ```
3. build the new tarballs in the `dist` directory:
    ```sh
    python -m build --sdist --outdir dist .
    ```

## To-do

- [ ] isocontour plotting
- [x] add streamplot for fieldline plotting
- [x] print all the newly added colormaps and the default color sequence
- [x] add a test plot for the demo
- [x] add image to readme
- [x] dark mode
- [x] monotype non-Latex mode
