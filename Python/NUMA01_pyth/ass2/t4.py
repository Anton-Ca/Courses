#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The purpose of this script is to investigate if a sequence converges.

@author: Anton Carlsson
"""


def main():
    """ Main function of the program. """
    x0 = 1
    alpha = [-0.5, 0.5, -0.25, 0.25]
    a1 = 0
    a2 = 1
    y = None
    for a in alpha:
        y = seq(a, x0)

        if abs(seq(a, y) - seq(, x)) < 1.e-9:

        x0 = y

    #while abs(seq(alpha[a2], x) - seq(alpha[a1], x)) < 1.e-9 and a2 <= 3:
    #    y = seq(alpha[a2], x)
    #    a1 += 1
    #    a2 += 2
        #x0 += 1

        #if a1 > 3:
        #    a1 = 0
        #if a2 > 3:
        #    a2 = 0
    msg1 = f"Sequence converged to x= {ans}"
    msg2 = "No convergence detected."


def seq(a: int, x: int):
    """
    Returns value of sequence given a and x.
    """
    xn = 0.2*x - a*(x**2 - 5)
    return xn


if __name__ == "__main__":
    main()

