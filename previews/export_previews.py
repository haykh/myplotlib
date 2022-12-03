import os
import matplotlib as mpl
import matplotlib.pyplot as plt

import myplotlib
import myplotlib.tests as mypltests

readme = ""

for st, fl in [
    f.replace(".mplstyle", "").split(".")
    for f in os.listdir("myplotlib/assets")
    if f.endswith(".mplstyle")
]:
    mpl.rcParams.update(mpl.rcParamsDefault)
    myplotlib.load(st, fl)
    mypltests.testAll()
    plt.savefig(f"previews/{st}_{fl}.jpg")
    readme += f"# `{st}.{fl}`\n\n![{st}_{fl}]({st}_{fl}.jpg)\n\n"

with open("previews/README.md", "w") as f:
    f.write(readme)
