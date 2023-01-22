#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The task is to experiment with list operations.
@author: Anton Carlsson
"""


from scipy import *
from matplotlib.pyplot import *
import sys


L = [1, 2]
L3 = 3*L

def main():
    print(L3[0])
    print(L3[-1])

    try:
        print(L3[10])
    except Exception:
        print("Error trying to print value outside list range.")



if __name__ == "__main__":
    main()

