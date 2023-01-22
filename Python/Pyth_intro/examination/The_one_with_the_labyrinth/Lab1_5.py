#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Author: Anton Carlsson
Course: DA557A ST22
Solution to: The one with the labyrinth
Examination: 1
Comment: I know you can do the lab even with a similar solution without numpy,
but I'm just more used to the syntax, hope that's ok. Also I got tired of making
doc-strings for this lab, but check out Lab1_3 for some cool doc-strings.
"""


import numpy as np


# Declaration of variables
# Constants
WALL = 0
PATH = 1
START = 2
EXIT = 3
TRAP = 4
POWER = 5
ORIGIN = [7, 2]
# Variables
life = 20
curr_pos = [7, 2]


def main():
    board = create_board()
    print_startup_msg()
    run_program(board)
    if get_board_val(board, curr_pos) != EXIT:
        print("Game over! You did not reach the exit in time.")


def print_startup_msg():
    start_msg = """You have been placed in a pitch-black labyrinth, without
    knowing if there is a way out or not. Maybe there are traps? The only
    option available is to walk in a random direction and hope for the best,
    hope that you do not walk into a wall, or even worse, that you walk in
    circles. But hurry up, you only have so many moves…"""
    print(
        "",
        start_msg,
        "",
        "To move around use:",
        "w = up",
        "a = left",
        "s = down",
        "d = right",
        "\n",
        sep="\n",
    )


def create_board() -> np.ndarray:
    # Initiating board with only walls
    board = np.zeros((10, 10))
    pths = [
        [1, 0],
        [2, 0],
        [3, 0],
        [4, 0],
        [5, 0],
        [6, 0],
        [7, 0],
        [8, 0],
        [9, 0],
        [1, 1],
        [9, 1],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [5, 2],
        [6, 2],
        [9, 2],
        [3, 3],
        [7, 3],
        [3, 4],
        [5, 4],
        [6, 4],
        [7, 4],
        [1, 5],
        [2, 5],
        [3, 5],
        [3, 6],
        [4, 6],
        [5, 6],
        [6, 6],
        [7, 6],
        [8, 6],
        [8, 7],
        [2, 8],
        [3, 8],
        [4, 8],
        [8, 8],
        [4, 9],
        [5, 9],
        [6, 9],
        [7, 9],
        [8, 9],
    ]
    s = [7, 2]
    e = [1, 8]
    t = [[9, 3], [1, 6], [2, 9]]
    p = [[1, 4], [6, 8]]

    # Setting up paths
    for path in pths:
        board[path[0]][path[1]] = PATH
    # Setting up traps
    for trap in t:
        board[trap[0]][trap[1]] = TRAP
    # Setting up power ups
    for power in p:
        board[power[0]][power[1]] = POWER
    # Select start position
    board[s[0]][s[1]] = START
    # Select exit position
    board[e[0]][e[1]] = EXIT

    return board


def get_board_val(board, current_pos):
    return board[current_pos[0]][current_pos[1]]


def run_program(board):
    global life

    # Continue while we have lives left and not yet found the exit
    while life > 0 and get_board_val(board, curr_pos) != EXIT:

        choice = input("Enter direction: ")

        # Controls for the game w=up, a=left, s=down, d=right
        if choice == "w":
            new_pos = [curr_pos[0] - 1, curr_pos[1]]
            move(board, new_pos)
        elif choice == "a":
            new_pos = [curr_pos[0], curr_pos[1] - 1]
            move(board, new_pos)
        elif choice == "s":
            new_pos = [curr_pos[0] + 1, curr_pos[1]]
            move(board, new_pos)
        elif choice == "d":
            new_pos = [curr_pos[0], curr_pos[1] + 1]
            move(board, new_pos)
        else:
            pass


def move(board, pos):
    global life
    global curr_pos

    # Makes sure we cannot move outside board
    if -1 in pos or 10 in pos:
        print("Ouch! I can not walk through walls...")
        return None

    val = get_board_val(board, pos)

    # Updates the game stage based on what square we are moving to
    if val == WALL:
        print("Ouch! I can not walk through walls...")
    elif val == PATH or val == START:
        life -= 1
        curr_pos = pos
    elif val == TRAP:
        life -= 1
        print("Oh no, a trap!")
        curr_pos = ORIGIN
    elif val == POWER:
        life -= 1
        print("A chocolate bar, I feel stronger.")
        curr_pos = pos
        life += 15
    else:
        print("You survived! Well done adventurer!")
        curr_pos = pos
        return None


if __name__ == "__main__":
    main()
