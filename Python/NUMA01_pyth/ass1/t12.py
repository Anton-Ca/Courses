#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The purpose of this script is to solve a recursion problem and
plot the result.

@author: Anton Carlsson
"""


from math import exp
from matplotlib import pyplot as plt


def main():
    """ Main function of the program. """
    h = 1 / 1000
    td = [ind for ind in range(0, int(1/h) + 1)]
    a = -0.5
    u = [exp(0), exp(h*a), exp(2*h*a)]
    nh = []
    y = []
    for ind in td:
        u1 = u[ind]
        u2 = u[ind+1]
        u3 = u[ind+2]
        u.append(u3+h*a*((23/12)*u3-(4/3)*u2+(5/12)*u1))
        nh.append(ind*h)
        y.append(exp(a*h*ind))
    diff = [abs(y[i]-u[i]) for i in td]

    plt.plot(nh, diff)
    plt.xlabel(r'$nh$', fontsize=14)
    plt.ylabel(r"$e^{ta}$", fontsize=14)
    plt.title(r"Recursion formula compared to $e^{ta}$")
    plt.show()


if __name__ == "__main__":
    main()

