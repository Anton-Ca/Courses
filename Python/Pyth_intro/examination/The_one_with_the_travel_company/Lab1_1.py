#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Anton Carlsson
Course: DA557A ST22
Solution to: The one with the travel company
Examination: 1
"""


# Declaration of variables
# Constants
BUDGET = 500
ECONOMY = 750
VIP = 2000
BAG = 200
MEAL = 150
# Variables
ticket = None
nbr_bags = 0
nbr_meals = 0


def main():
    """Main function to run the program."""
    display_greeting_menue()
    choice = input("Your choice >> ")
    generate_ticket(choice)
    initiate_session()


def generate_ticket(choice):
    """Takes in a string choice and generates a ticket for the user."""
    global ticket
    if choice == "1":
        ticket = BUDGET
    elif choice == "2":
        ticket = ECONOMY
    elif choice == "3":
        ticket = VIP
    else:
        choice = input(
            ("Error not a valid choice! Please choose a number between 1 and 3 >> ")
        )
        generate_ticket(choice)


def display_greeting_menue():
    """Displays the startup menue for the user."""
    print("Ticket types:")
    print(f"1. Budget ( {BUDGET}kr)")
    print(f"2. Economy ( {ECONOMY}kr)")
    print(f"3. VIP ( {VIP}kr)\n")


def display_order():
    """Displays the users current order status."""
    print("\nCurrently you have:")
    print(f"\t {nbr_bags} bag(s) registered".expandtabs(4))
    print(f"\t {nbr_meals} meal(s) registered\n".expandtabs(4))


def display_options_menue():
    """Displays which options the user has."""
    print(
        "",
        "Here are your options:",
        "1. Add bag (max 1)",
        "2. Add meal (max 1)",
        "3. Remove bag",
        "4. Remove meal",
        "5. Finalize ticket",
        sep="\n",
    )


def print_receipt():
    """Takes in string ticket and prints a receipt for the user."""
    str_len = 7
    t = "Ticket"
    b = "Bag"
    m = "Meal"
    tot = "Total"
    print("\nReceipt:")
    print(t + " " * (str_len - len(t)) + ":", f"{ticket:>4}kr")
    total = ticket
    if nbr_bags != 0:
        print(b + " " * (str_len - len(b)) + ":", f"{BAG:>4}kr")
        total += BAG
    if nbr_meals != 0:
        print(m + " " * (str_len - len(m)) + ":", f"{MEAL:>4}kr")
        total += MEAL
    print(" " * 7, "-" * 7)
    print(tot + " " * (str_len - len(tot)) + ":", f"{total:>4}kr\n")


def run_program(choice):
    """Takes in a string choice and determines the right operations based on the users choice."""
    global nbr_bags
    global nbr_meals

    if choice == "1":
        nbr_bags = 1
        initiate_session()
    elif choice == "2":
        nbr_meals = 1
        initiate_session()
    elif choice == "3":
        nbr_bags = 0
        initiate_session()
    elif choice == "4":
        nbr_meals = 0
        initiate_session()
    elif choice == "5":
        print_receipt()
    else:
        choice = input(
            ("Error not a valid choice! Please choose a number between 1 and 5 >> ")
        )
        run_program(choice)


def initiate_session():
    """Updates the users order status and let's the user make further choices."""
    display_order()
    display_options_menue()
    choice = input("Your choice >> ")
    run_program(choice)


if __name__ == "__main__":
    main()
