#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The purpose of this script is to...

@author: Anton Carlsson
"""


from t3 import L3
from t4 import L4


L5 = L3
L5.extend(L4)


def main():
    print(f"L5: {L5}")


if __name__ == "__main__":
    main()

