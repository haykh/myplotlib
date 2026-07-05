import matplotlib.pyplot as plt

from myplotlib import _STYLE_RECIPES
import myplotlib.tests as mypltests
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--styles",
        default=[],
        nargs="*",
        help="List of styles to generate previews for",
    )
    args = parser.parse_args()

    readme = ""

    styles = args.styles if args.styles else list(_STYLE_RECIPES.keys()) + ["plain"]
    for style in styles:
        fname = style.replace(".", "_")
        ctx = plt.style.context(style) if style != "plain" else plt.rc_context()
        with ctx:
            mypltests.testAll()
            plt.savefig(f"previews/{fname}.png")
            plt.close("all")
            readme += f"# `{style}`\n\n![{fname}]({fname}.png)\n\n"

    if not args.styles:
        with open("previews/README.md", "w") as f:
            f.write(readme)
