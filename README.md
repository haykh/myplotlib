# `myplotlib`

`matplotlib` binder with custom styles and routines for fast plotting. see [previews of available styles](https://github.com/haykh/myplotlib/tree/master/previews#readme).

### installation

```shell
pip install myplotlib
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

### development

Building tarballs in the `dist` directory:

```sh
python -m build --sdist --outdir dist .
```

### To-do

- [ ] isocontour plotting
- [x] add streamplot for fieldline plotting
- [x] print all the newly added colormaps and the default color sequence
- [x] add a test plot for the demo
- [x] add image to readme
- [x] dark mode
- [x] monotype non-Latex mode
