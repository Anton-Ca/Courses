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
import pickle
import re

TRANSLATION = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


def main():
    """
    Main function to run the program. Prints out the reversed bubble sort of to lists.
    """
    filenames = sys.argv[1:]
    try:
        orders = read_orders(filenames[0])
        valid_words = read_words(filenames[1])
    except Exception as err:
        print("Error: There was a problem with at least one of the files.")
        err = None
        return err

    possible_combinations = []
    words = []

    for order_number in orders:
        possible_combinations = find_all_possible_combinations(order_number)
        words = filter_valid_words(possible_combinations, valid_words)
        display_possible_words(order_number, words)


def read_orders(filename: str) -> set:
    """
    Opens the file linked by the string filename.
    Reads and returns the Set of order numbers stored in the file using pickle.
    """
    orders = None
    with open(filename, "rb") as infile:
        orders = pickle.load(infile)

    return orders


def read_words(filename: str) -> list:
    """
    Reads file filename and returns a list of it's words.
    """
    lines = None
    with open(filename) as infile:
        lines = infile.readlines()
        lines = [re.sub(r"[\s]+", "", line) for line in lines]
    return lines


def find_all_possible_combinations(order_number: str) -> list:
    """
    This function returns all the possible combinations that can be
    achieved using the digits in the order_number string.
    """
    combinations = []
    for digit in order_number:
        combinations = add_digit(digit, combinations)
    return combinations


def add_digit(digit: str, combinations: list) -> list:
    """
    The two parameters are the next digit to add and the current
    collection of combinations found. Returned is all new combinations
    found by adding the new digit.
    """
    letters = TRANSLATION.get(digit)
    new_combinations = []

    if len(combinations) == 0:
        if letters is not None:
            for letter in letters:
                new_combinations.append(letter)
        return new_combinations

    for cmb in combinations:
        for let in letters:
            new_combinations.append((cmb + let))
    return new_combinations


def filter_valid_words(possible_combinations: list, valid_words: set) -> list:
    """
    The function returns all combinations from possible_combinations
    that also exists in valid_words.
    """
    valid = []
    valid_combinations = []
    for word in possible_combinations:
        if word in valid_words:
            valid.append(word)
    valid_combinations.extend(valid)

    return valid_combinations


def display_possible_words(order_number: str, words: list):
    """
    This function is responsible for displaying one order_number
    and the potential real words it can translate into.
    """
    if words != []:
        print()
        print(order_number + " : ", end="")
        print(words[0])
        for word in words:
            if len(words) > 1 and word != words[0]:
                print("        " + word)
    else:
        print()
        print("00000 : No real word found.")


if __name__ == "__main__":
    main()
