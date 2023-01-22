#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The purpose of this script is to make a plot of yplot versus xplot.
Use for this the command plot. Dependingon your environment, you might
also need to run show() to show the plot.

@author: Anton Carlsson
"""


import t8
import t9
from matplotlib import pyplot as plt


def main():
    """ Main function of the program. """
    x = t8.main()
    y = t9.main()
    plt.plot(x,y)
    plt.show()


if __name__ == "__main__":
    main()

