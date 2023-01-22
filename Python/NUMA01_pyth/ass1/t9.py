#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The purpose of this script is to set up a list yplot
which contains the values arctan(x) for all the x in xplot.

@author: Anton Carlsson
"""


import t8
import numpy as np


def main():
    """ Main function of the program. """
    x = t8.main()
    y = np.arctan(x)
    print(y)
    return y




if __name__ == "__main__":
    main()

