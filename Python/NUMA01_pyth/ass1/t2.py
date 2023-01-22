#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The purpose of this script is to Check whether the expression
x^2 + 0.25x − 5 is zero for x = 2.3.
@author: Anton Carlsson
"""


from scipy import *
from matplotlib.pyplot import *
import sys


def main():
    x = 2.3
    y = x**2+0.25*x-5
    if y == 0.0:
        print("The expression is zero for x = 2.3")
    else:
        print("The expression is not zero for x = 2.3")



if __name__ == "__main__":
    main()

