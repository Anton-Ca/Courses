#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Author: Anton Carlsson
Course: DA557A ST22
Solution to: The one where numbers needs to be sorted
Examination: 1
Comment: I'm lazy so I did low effort doc-strings.
"""


import sys
import re


def main():
    """
    Main function to run the program. Prints out the reversed bubble sort of to lists.
    """
    filenames = sys.argv[1:]
    numbers = []
    for nbr, filename in enumerate(filenames):
        nbrs = read_file(filename)
        nbrs = filter_odd_or_even(nbrs, nbr == 0)
        numbers.extend(nbrs)
    numbers = reversed_bubble_sort(numbers)
    print(numbers)


def read_file(filename):
    """
    Reads file filename and returns a list of it's numbers (assumes integers).
    """
    numbers = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            line = re.sub(r"[^\S]+", " ", line)
            nbrs = line.split(" ")
            nbrs = list(filter(None, nbrs))
            for nbr in nbrs:
                numbers.append(nbr)
    numbers = [int(x) for x in numbers]
    return numbers


def filter_odd_or_even(numbers: list, odd: bool) -> list:
    """
    Filters out all numbers that are odd or even depending on bool odd.
    """
    return list(filter(lambda x: x % 2 != 0 if odd else x % 2 == 0, numbers))


def reversed_bubble_sort(numbers: list) -> list:
    """
    Takes in a list called numbers and returns the reversed bubble sorted list.
    """
    n = len(numbers)
    swapped = False
    while not swapped:
        swapped = True
        for i in range(1, n):
            nbr1 = numbers[i - 1]
            nbr2 = numbers[i]
            if nbr1 < nbr2:
                numbers[i] = nbr1
                numbers[i - 1] = nbr2
                swapped = False
    return numbers


if __name__ == "__main__":
    main()
