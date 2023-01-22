#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The purpose of this script is to use the command range and
a list comprehension to generate a list with 100 equidistantly
spaced values between (and including) 0 and 1.

@author: Anton Carlsson
"""


from numpy import linspace as lin


# lst = lin(0, 1, 100) # Did not read instructions, but this is better solution


step = (1 - 0) * 1 / 99
lst = [x*step for x in range(0,99)]
lst.extend([1])
def main():
    print(lst)

if __name__ == "__main__":
    main()
