#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The purpose of this script is to make equally spaced list with for loop.

@author: Anton Carlsson
"""


# Import variable by:
# import filename
# var = filename.main()
def main():
    """ Main function of the program. """
    global xplot
    xplot = []
    step = (1 - 0) * 1 / 99
    for ind in range(0,99):
        xplot.append(ind*step)
    xplot.append(1)
    print(xplot)
    return xplot


if __name__ == "__main__":
    main()

