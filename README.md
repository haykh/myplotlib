# `myplotlib v0.9.4`

`matplotlib` binder with custom styles. see [previews of available styles](myplotlib/previews).

### installation

```shell
pip install git+https://github.com/haykh/myplotlib.git@master
```

### usage

```python
# initialize style:
import myplotlib
myplotlib.load(style=..., flavor=...)
# style can be [`fancy` | `mono` | `hershey`]
# flavor can be [`light` | `dark`]
# if not specified defaults to `style = 'main', flavor = 'light'`

# auxiliary functions for plotting:
import myplotlib.plots as myplt
# type for docstring:
myplt?

# preview custom styles with built-in functions
import myplotlib.tests as mypltest
# type for docstring:
mypltest?
```

for more usage examples checkout the `tests/` submodule.

### requirements

* `python >= 3.6`
* `matplotlib >= 3.0.0`, `numpy`, `numba`
* `latex` (used for `style="fancy"` only)

### Latest updates
* `0.9.4r2` [Mar 2022]
  - better `hershey` font
  - fallback cursive font added
* `v0.9.4` [Mar 2022]
  - new `hershey` style a-la IDL
  - minor bug fixes in auto-determining the plot ranges
  - PEP 8 compatible style

### To-do

- [ ] isocontour plotting
- [x] add streamplot for fieldline plotting
- [x] print all the newly added colormaps and the default color sequence
- [x] add a test plot for the demo
- [x] add image to readme
- [x] dark mode
- [x] monotype non-Latex mode
