#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Anton Carlsson
Course: DA557A ST22
Solution to: The one where money need to be transported
Examination: 1
Comment: I understand that this excerise probably is supposed to only deal with
integers, but I thought that was unnessesarily limiting, so I hope I don't get
deductions for accepting any input (including float numbers).
Also: If your exammining this you'll find the function calc_plan with the loops
at line 153.
"""

import math
import re


# Declaration of variables
# Constants
BIG = 80
BCOST = 60000
MEDIUM = 50
MCOST = 30000
SMALL = 20
SCOST = 10000
# Variables
summed_volume = 0
original_volume = 0
nbr_big = 0
nbr_medium = 0
nbr_small = 0


def main():
    """
    Main function to run the program.
    """
    display_greeting_message()
    volume = get_volume()
    print_packing_plan(volume)


def display_greeting_message():
    """
    Displays the startup message for the user.
    """
    welcome_msg = "Welcome to the Money Bag Transport Calculator (M.B.T.C)"
    print(
        "",
        welcome_msg,
        "-" * len(welcome_msg),
        "",
        sep="\n",
    )


def get_volume() -> int:
    """
    Reads a volume from the input, confirms that it's larger than or equal to
    100 and then returns it as an integer.

    Returns
    -------
    volume : int
        Total capacity before any bags have been packed.
    """

    global original_volume

    # Using regex to take care if user inserts number with wrong decimal symbol
    volume = re.sub(",", ".", input("What is the volume of the truck (>= 100): "))

    # Checks that the volume is convertible to a float
    if not isfloat(volume):
        return get_volume()

    # Checks that the volume is larger than or equal to 100L
    if float(volume) < 100:
        return get_volume()

    original_volume = float(volume)
    volume = convert_to_int(volume)

    return volume


def isfloat(value: str) -> bool:
    """
    Determines whether it's possible to convert a string value into a float number.

    Parameters
    ----------
    value : str
        A string version of a number example "420.69".

    Returns
    -------
        True or false depending on if the parameter value can be converted into a float.
    """

    try:
        float(value)
        return True
    except ValueError:
        return False


def convert_to_int(value: str) -> int:
    """
    Converts a string value into an upper limit rounded integer.

    Parameters
    ----------
    value : str
        A string version of a number example "420.69".

    Returns
    -------
        An integer rounded to the upper limit.
    """

    return int(math.ceil(float(value)))


def print_packing_plan(volume: int):
    """
    Prints amounts of different bags that should be packed as well as how
    much space is left and what the total value is. Returns nothing.

    Parameters
    ----------
    volume : int
        Total capacity before packing any bags.
    """

    total_value, space_left = calc_plan(volume)
    # plan_name and space_l are only used for pretty formatting
    plan_name = "Packing plan"
    space_l = (
        int(space_left)
        if space_left == math.floor(space_left)
        else "{:.2f}".format(space_left)
    )
    print(
        "",
        plan_name,
        "-" * len(plan_name),
        f"{nbr_big:>1} big bags",
        f"{nbr_medium:>1} medium bags",
        f"{nbr_small:>1} small bags",
        "",
        f"Space left : {space_l:>2}L",
        f"Total value: {total_value:>2}kr\n",
        sep="\n",
    )


def calc_plan(volume: int):
    """
    The function calculates all values needed to print a packing plan.

    Parameters
    ----------
    volume : int
        Volume capacity of the truck.

    Returns
    -------
    total_value : int
        Calculate total value of bags in truck.
    space_left : int
        Calculate space left in truck.

    Comment:
    --------
    This function should probably be devided up into many sub-functions to
    improve readability. But fk it, nobody remembers a readability wussy.
    """
    global summed_volume
    global nbr_big
    global nbr_medium
    global nbr_small

    # Calculate for big bags (loop 1)
    for _ in range(volume, MEDIUM, -BIG):
        if (volume - summed_volume) < BIG:
            break
        nbr_big += 1
        summed_volume += BIG

    # Calculate for medium bags (loop 2)
    for _ in range(volume - nbr_big * BIG, SMALL, -MEDIUM):
        if (volume - summed_volume) < MEDIUM:
            break
        nbr_medium += 1
        summed_volume += MEDIUM

    # Calculate for small bags (loop 3)
    for _ in range(volume - nbr_medium * MEDIUM - nbr_big * BIG, 0, -SMALL):
        if (volume - summed_volume) < SMALL:
            break
        nbr_small += 1
        summed_volume += SMALL

    space_left = original_volume - summed_volume
    total_value = nbr_big * BCOST + nbr_medium * MCOST + nbr_small * SCOST

    return total_value, space_left


if __name__ == "__main__":
    main()
