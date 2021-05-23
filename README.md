# myplotlib

`matplotlib` binder with custom styles.

![preview](https://github.com/haykh/myplotlib/blob/master/myplotlib/preview.jpg)

### installation

```shell
pip install git+https://github.com/haykh/myplotlib.git@master
```

### usage

```python
import myplotlib
# initialize styles:
myplotlib.load()

import myplotlib.plots as mypl
# type for docstring:
mypl? 
```

### requirements

* `matplotlib>=3.0.0`, `numpy`, `scipy`
* `latex` (install separately)

### To-do

- [ ] add streamplot for fieldline plotting 
- [ ] isocontour plotting
- [ ] add a test plot for the demo
- [ ] add image to readme
- [ ] print all the newly added colormaps and the default color sequence
