#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
What does the following command do?
L4 = [k**2 for k in L3]

@author: Anton Carlsson
"""
from t3 import L3



L4 = [k**2 for k in L3]
def main():
    print("L4 is each element of list L3 squared by 2,",
            "which should correspond to: [1, 4, 1, 4, 1, 4]",
            sep = "\n")
    print(f"\nThe correct value is {L4}")



if __name__ == "__main__":
    main()

