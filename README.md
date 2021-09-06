# `myplotlib v0.9.1`

`matplotlib` binder with custom styles.

![preview](https://github.com/haykh/myplotlib/blob/master/myplotlib/preview.jpg)

### installation

```shell
pip install git+https://github.com/haykh/myplotlib.git@master
```

### usage

```python
# initialize styles:
import myplotlib
myplotlib.load()

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

* `matplotlib>=3.0.0`, `numpy`, `scipy`, `numba`
* `latex` (install separately)

### To-do

- [x] add streamplot for fieldline plotting
- [x] print all the newly added colormaps and the default color sequence
- [x] add a test plot for the demo
- [x] add image to readme
- [ ] isocontour plotting
- [x] dark mode
- [ ] monotype non-Latex mode
