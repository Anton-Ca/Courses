#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The purpose of this script is to...

@author: Anton Carlsson
"""


def main():
    """ Main function of the program. """

    # Prints the sum of the sum of all previous numbers starting from 0
    # up to 500 and the curret number
    s = 0
    for i in range(0, 500):
        s = s + i
        #print(s)

    # Prints a list where each number s in the above method is concatenated
    ss = [0]
    for i in range(1, 500):
        ss.append(ss[i-1] + i)
        #print(ss)

    print(s)

if __name__ == "__main__":
    main()

