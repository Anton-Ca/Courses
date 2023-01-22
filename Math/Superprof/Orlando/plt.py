#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from matplotlib.pyplot import *
from matplotlib import style, rc, rcParams
from math import *
from sympy import symbols
from sympy.plotting import plot as symplot


"""
The purpose of this script is to plot different functions.
Reveal answers to what the function is by setting show_ans to True.

@author: Anton Carlsson
"""


show_ans = True


def main():
    """Main function of the program."""

    x = symbols("x")
    y = -1/2*x + 3

    customize_plot()
    symplot(
        y,                      # Function to plot
        xlabel="$x$",
        ylabel="$y$",
        xlim=[-8, 8],
        ylim=[-6, 6],
        #legend=show_ans,
        axis=True,
    )


def customize_plot() -> None:
    """Customizes plot"""

    style.use("seaborn-whitegrid")
    rcParams["axes.linewidth"] = 1.5
    rcParams["axes.labelsize"] = 24
    rcParams["xtick.labelsize"] = 16
    rcParams["ytick.labelsize"] = 16
    rcParams["axes.edgecolor"] = "black"
    rcParams["lines.linewidth"] = 3
    rcParams["legend.loc"] = "best"
    rcParams["legend.frameon"] = True


if __name__ == "__main__":
    main()
