#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The purpose is to solve the first homework assignment and
to approximate the log-function by an iteration methods.

@Author: Anton Carlsson, Natalia Timokhova
"""


from math import *
from numpy import *
from matplotlib.pyplot import *


def main():
    """Main function of the program. Selects which task to run."""

    task_1()  # Change this line if we want to run a different task


# |------------------------------ Task 1 ------------------------------|#


def task_1():
    """Solution to task 1."""

    x = 1.41
    print(f"\nDen approximativa lösningen är:  {approx_ln(x)}")
    print(f"Den exakta lösningen är: \t {log(x)}\n")


def approx_ln(x: float, n = 3) -> float:   # "x: float" we expect float as input
                                            # but it's not required. Same with
                                            # "-> float" but for return.
    """
    Approximates the logarithm with n steps.

    @parameter x : int (Value to estimate the logarithm for)
    @parameter n : int (Number of iterations)
    @returns estimated_ln : int (Approximated ln for the value x)
    """

    # Raise value error if restrictions are not followed
    if not x > 0 or not n >= 1:
        raise ValueError("Error! Please follow restrictions x > 0, and n >= 1.")

    # Initialization variables
    a = (1 + x) / 2
    g = sqrt(x)

    # Iteratively updates variables
    for ind in range(n):
        a = (a + g) / 2
        g = sqrt(a * g)

    # Approximation formula for logarithm
    estimated_ln = (x - 1) / a

    return float(estimated_ln)


# |------------------------------ Task 2 ------------------------------|#


def task_2():
    """Solution to task 2."""

    xx = linspace(1, 10, num=10)        # Increase num for smoother plot curves
    nn = [1, 2, 3, 9]                   # Different amount of iterations we
                                        # want to try.
    ln = [log(i) for i in xx]           # Exact logarithmic values
    ind = 0                             # ind used to create to separate figures

    # Plot for each amount of iterations
    for n in nn:
        approx = []
        difference = []
        # Calculate approximation and difference for all points
        for x in xx:
            approx.append(approx_ln(x, n))
            difference.append(abs(log(x) - approx_ln(x, n)))

        # First figure (shows exact and estimated functions)
        figure(ind)
        plot(xx, approx, label=f"n={n}")
        plot(xx, ln, label=r"$ln(x)$")
        xlabel(r"$x$")
        ylabel(r"$approx\_ln(x)$")
        title(r"Approximations of $\ln{(x)}$")
        legend()
        show()

        # Second figure (Shows difference between estimated and exact function)
        figure(ind + 1)
        plot(xx, difference, label=fr"$n={n}$")
        xlabel(r"$x$")
        ylabel(r"$|ln(x) - approx\_ln(x)|$")
        title("Difference between ln(x) and the approximation mathod.")
        legend()
        show()

        ind += 2


# |------------------------------ Task 3 ------------------------------|#


def task_3():
    """Solution to task 3."""

    x = 1.41
    n = 5
    # Plot versus n meaning we want x-axis to be n values
    nn = linspace(1, n, num=n)
    difference = []

    # Calculate error for different n values
    for n in nn:
        difference.append(abs(log(x) - approx_ln(x, int(n))))

    # Plot error as function of n where the error is
    # abs(ln(x) - approx_ln(x))
    figure(0)
    plot(nn, difference)
    xlabel(r"$n$")
    ylabel(r"$|ln(x) - approx\_ln(x)|$")
    title("Difference between ln(x) and the approximation mathod.")
    show()


def task_4():
    """Solution to task 4."""

    x = 1.41
    print(f"\nApproximerad lösning:\t {fast_approx_ln(x)}")
    print(f"Exakt logaritm: \t {log(x)}\n")


def fast_approx_ln(x: float, n=3) -> float:
    """
    Approximates the logarithm using B.C. Carlssons algorithm with n steps.

    @parameter x : int (Value to estimate the logarithm for)
    @parameter n : int (Number of iterations)
    @returns estimated_ln : int (Approximated ln for the value x)
    """

    # Raise value error if restrictions are not followed
    if not x > 0 or not n >= 1:
        raise ValueError("Error! Please follow restrictions x > 0, and n >= 1.")

    # Approximation algorithm where d is defined below
    estimated_ln = (x - 1) / d(x, n, n)

    return float(estimated_ln)


def d(x: float, k: int, i: int) -> float:
    """
    Docstring function explanation

    @parameter x : int (Value to estimate the logarithm for)
    @parameter n : int (Number of iterations)
    @returns estimated_ln : int (Approximated ln for the value x)
    """
    # Initialize variables
    a = (1 + x) / 2
    g = sqrt(x)

    # k < 1 means we have reached our base case and should return ai
    if k < 1:
        # Iterate i times and update the value of a to get ai
        for _ in range(i):
            a = (a + g) / 2
            g = sqrt(a * g)
        return a
    else:
        # If not base case we instead return the formula for dki
        return (d(x, k-1, i) - 4**(-k) * d(x, k-1, i-1)) / (1 - 4**(-k))


def task_5():
    """Solution to task 5."""
    # Plot versus x, but try different n values
    n = [2, 3, 4, 5]
    xx = linspace(1, 20, num=69)

    for i in n:
        difference = []
        # Calculate error for all points given a value for n
        for x in xx:
            difference.append(abs(log(x) - fast_approx_ln(x, i)))

        # Make sure to plot for different n in same figure
        figure(0)
        plot(xx, difference, label=f"{i} iterations")

    # Make figure pretty :)
    figure(0)
    semilogy()
    xlabel(r"$x$")
    ylabel("Error")
    axis([-1, 20, 1.0e-19, 1.0e-2])
    xticks(np.arange(0, 21, 5))
    title("Error behavior of the accelerated Carlsson Method for the log")
    legend()
    show()


if __name__ == "__main__":
    main()
