#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The purpose of this script is to print results from recursion task 1.

@author: Anton Carlsson
"""


from numpy import linspace
from matplotlib import pyplot as plt
from math import sin


def main():
    """ Main function of the program. """
    a = 0.5
    x = linspace(5, 30)
    y = []
    y.append([sin(i)-a*i+30 for i in x])

    plt.plot(x, y[0])
    plt.xlabel(r'X', fontsize=14)
    plt.ylabel(r"Y", fontsize=14)
    plt.title(r"Title")
    plt.show()



if __name__ == "__main__":
    main()

