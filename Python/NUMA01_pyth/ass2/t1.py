#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The purpose of this script is to examine recursion behavior.

@author: Anton Carlsson
"""


from math import sin


def main():
    """ Main function of the program. """
    x=0.5
    a=[0.5, 8.0]
    small = False
    for aa in a:
        print(f"Testing for a = {aa}")
        for i in range ( 200 ):
            p1 = x
            p2 = sin(x)
            p3 = aa*x
            ptot = abs(p1-(p2-p3+30))
            if ptot < 1.e-8:
                small = True
                print(r"Equation < 1.e-8")
                break
            x=sin(x)-aa*x+30
        if not small:
            print ( f"The result after {i+1} iterations is {x}")
        small = False


if __name__ == "__main__":
    main()

