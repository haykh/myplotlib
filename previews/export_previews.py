import os
import logging
import matplotlib.pyplot as plt

import myplotlib.tests as mypltests
import argparse


class _P22WeightWarningFilter(logging.Filter):
    def filter(self, record):
        return record.getMessage() != (
            "findfont: Failed to find font weight bold, now using 400."
        )


logging.getLogger("matplotlib.font_manager").addFilter(_P22WeightWarningFilter())

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

    styles = sorted(
        f.replace(".mplstyle", "")
        for f in os.listdir("myplotlib/assets")
        if f.endswith(".mplstyle")
        and (not args.styles or f.replace(".mplstyle", "") in args.styles)
    )
    if not args.styles:
        styles += ["plain"]
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
