#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The purpose of this script is to compute the sum of the square
root of all integers up to 200.

@author: Anton Carlsson
"""


import math



def main():
    """ Main function of the program. """
    tot = 0.0
    for ind in range(1,200):
        tot += 1.0 / math.sqrt(ind)
    print(tot)



if __name__ == "__main__":
    main()

