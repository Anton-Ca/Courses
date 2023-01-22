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


def main() -> None:
    """
    Main function to run the program. Prints out the reversed bubble sort of to lists.
    """
    filenames = sys.argv[1:]
    try:
        for filename in filenames:
            list_of_strings = read_lines(filename)
    except Exception as err:
        print("An error occurred while trying to read the file.")
        err = None
        return err
    cars = parse_cars(list_of_strings)
    distance = re.sub(",", ".", input("How far do you want to drive (kilometers)? "))
    percentages = calculate_percentage(distance, cars)
    if percentages is None:
        return None
    display_result(percentages)
    return None


def read_lines(filename: str) -> list:
    """
    This function shall read all the lines from a file, strip them of
    the new line character, and place them in a list that is returned.
    """
    lines = None
    with open(filename) as infile:
        lines = infile.readlines()
        lines = [re.sub("[\n]+", "", line) for line in lines]
    return lines


def parse_cars(list_of_strings: list) -> list:
    """
    Processes a list of strings list_of_strings and returns the car model
    and max range as a tuple in the list cars.
    """
    cars = []
    for string in list_of_strings:
        parsed = string.split(":")
        cars.append((parsed[0], int(parsed[1])))
    return cars


def calculate_percentage(distance: int, cars: list) -> list:
    """
    Takes in int distance and list cars to return a list of car models and
    their max range.
    """
    if isfloat(distance):
        distance = float(distance)
    else:
        return None

    percentages = []
    for car in cars:
        percentage = distance / car[1] * 100
        percentages.append((car[0], percentage))

    return percentages


def display_result(percentages: list):
    """
    Takes as a parameter a list of tuples where each tuple contains
    the name of the car model a percentage (as a Float). The function
    shall display a header and a list on the screen.
    """
    print(
        "To drive the specified distance would correspond to this many\n",
        "percent of each cars specified max range.",
        sep="",
    )
    example_string = "Tesla Model S Long Range             "
    string_length = len(example_string)
    for car in percentages:
        perc = (
            f"{round(car[1])}%"
            if car[1] <= 100
            else f"Distance exceeds max range ({round(car[1])}%)"
        )
        print(car[0] + " " * (string_length - len(car[0])) + "-->  " + perc)


def isfloat(value: str) -> bool:
    """
    Determines whether it's possible to convert a string value into a float number.
    """

    try:
        float(value)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    main()
