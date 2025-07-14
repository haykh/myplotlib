import os
import matplotlib.pyplot as plt

import myplotlib
import myplotlib.tests as mypltests

if __name__ == "__main__":
    readme = ""

    for st, fl in [
        f.replace(".mplstyle", "").split(".")
        for f in os.listdir("myplotlib/assets")
        if f.endswith(".mplstyle") and f.count(".") == 2
    ]:
        with plt.style.context(f"{st}.{fl}"):
            mypltests.testAll()
            plt.savefig(f"previews/{st}_{fl}.png", dpi=300)
            readme += f"# `{st}.{fl}`\n\n![{st}_{fl}]({st}_{fl}.png)\n\n"

    with plt.style.context("latex"):
        mypltests.testAll()
        plt.savefig(f"previews/latex.png", dpi=300)
        readme += f"# `Latex`\n\n![Latex](latex.png)\n\n"

    mypltests.testAll()
    plt.savefig(f"previews/plain.png", dpi=300)
    readme += f"# `Plain`\n\n![Plain](plain.png)\n\n"

    with open("previews/README.md", "w") as f:
        f.write(readme)
