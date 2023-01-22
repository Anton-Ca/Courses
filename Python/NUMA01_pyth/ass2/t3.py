#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The purpose of this script is to do stuff.

@author: Anton Carlsson
"""


from math import sin



def main():
    """ Main function of the program. """
    x = 1
    y = []
    while func(x) > 1.e-9:
        y.append(x)
        x += 1
    print(len(y))
    return y



def func(x):
    """
    Function of the variable x.
    """
    return ((sin(x))**2)/x



if __name__ == "__main__":
    main()

