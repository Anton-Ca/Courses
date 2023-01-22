#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The purpose is to solve the second homework assignment and
to create an Interval class and implement arithmetic operations.

@Author: Anton Carlsson, Natalia Timokhova
"""


from numpy import *
from matplotlib.pyplot import *


def main():
    """Main function of the program. Selects which task to run."""
    Interval(1, 2)  # This does not work since __repr__ only works for
                    # interactive python shells, so instead run
                    # ./check3.sh in terminal (does the same but
                    # in an interactive python environment)

    check_task_3()
    check_task_4()
    check_task_8()
    check_task_9()
    task_10()


# |------------------------------ Task 1 ------------------------------|#


class Interval:
    """
    Class representing the interval of two real numbers initialized
    with a lower left endpoint and a higher right enpoint.
    """

    def __init__(self, left, *right):

        self.left = left

        # |---------------- Task 7 ----------------|#

        # No right argument meaning degenerate interval (task 7)
        if not len(right) > 0:
            self.right = left
        else:
            # Raise value error if left is not smaller than right enpoint
            if left > right[0]:
                raise ValueError("Left bound must be to less than right bound.")
            self.right = right[0]

    # |------------------------------ Task 2 ------------------------------|#

    def __add__(self, new):  # If name of function is right this will
                             # overload operator "+" to be compatible
                             # for class.
        """
        Interval representation of the arithmetic operation addition.

        parameter new : Interval (Interval for which endpoints should be added)
        returns _ : Interval (The new Interval after adding endpoints)
        """

        # If both objects are Intervals a, b, c and d are defined
        if isinstance(new, Interval):
            a, b, c, d = self.left, self.right, new.left, new.right
            return Interval(a + c, b + d)
        else:
            # new should in this case be a number and then it's just
            # added to the boundaries
            return Interval(self.left + new, self.right + new)

    def __radd__(self, new):
        """
        Interval representation of the arithmetic operation addition.
        When performed with an number example: 1 + Interval(1, 2)

        parameter new : int, float (Integer to be added to interval enpoints)
        returns _ : Interval (The new Interval after adding endpoints)
        """
        return self.__add__(new)

    def __sub__(self, new):
        """
        Interval representation of the arithmetic operation subtraction.

        parameter new : Interval (Interval for which endpoints
                        should be subtracted)
        returns _ : Interval (The new Interval after subtracting
                    endpoints)
        """

        if isinstance(new, Interval):
            a, b, c, d = self.left, self.right, new.left, new.right
            return Interval(a - d, b - c)
        else:
            return Interval(self.left - new, self.right - new)

    def __rsub__(self, new):
        """
        Interval representation of the arithmetic operation subtraction.
        When performed with an number example: 1 - Interval(1, 2)

        parameter new : int, float (Integer to be subtracted to interval enpoints)
        returns _ : Interval (The new Interval after subtracting endpoints)
        """
        return Interval(new).__sub__(self)

    def __mul__(self, new):
        """
        Interval representation of the arithmetic operation
        multiplication.

        parameter new : Interval (Interval for which endpoints
                        should be multiplication)
        returns _ : Interval (The new Interval after multiplying
                    endpoints)
        """

        if isinstance(new, Interval):
            a, b, c, d = self.left, self.right, new.left, new.right
            left = min([a * c, a * d, b * c, b * d])
            right = max([a * c, a * d, b * c, b * d])
            return Interval(left, right)

        # If int is less than zero enpoints needs to switch order
        elif new < 0:
            return Interval(self.right * new, self.left * new)

        else:
            return Interval(self.left * new, self.right * new)

    def __rmul__(self, new):
        """
        Interval representation of the arithmetic operation multiplication.
        When performed with an integer as: int * Interval

        parameter new : int, float (Integer to be multiplied to interval enpoints)
        returns _ : Interval (The new Interval after multiplying endpoints)
        """
        return self.__mul__(new)

    def __truediv__(self, new):
        """
        Interval representation of the arithmetic operation division.

        parameter new : Interval (Interval for which endpoints
                        should be division)
        returns _ : Interval (The new Interval after dividing
                    endpoints)
        """

        a, b, c, d = self.left, self.right, new.left, new.right

        # |---------------- Task 6 ----------------|#

        # If c or d is less than 10^(-15) division is approximately very large
        if abs(c) < 1.0e-15 or abs(d) < 1.0e-15:
            raise ValueError(
                """Error! Values after division are getting too large,
                choose a new Interval to divide with!"""
            )

        left = min([a / c, a / d, b / c, b / d])
        right = max([a / c, a / d, b / c, b / d])

        return Interval(left, right)

    # |------------------------------ Task 3 ------------------------------|#
    # Check by running the following command in a terminal window
    # ./check3.sh
    # or run check_task_3() function

    def __repr__(self):
        """
        Displays representation of the class to the user
        """
        return f"{[self.left, self.right]}"

    # |------------------------------ Task 4 ------------------------------|#
    # Check by running the following command in a terminal window
    # ./check4.sh

    # |------------------------------ Task 5 ------------------------------|#

    def __contains__(self, val) -> bool:
        """
        Checks if a real value is within the given interval.

        parameter val : float (Value potentially in interval)
        returns _ : bool (Wheter val in the interval or not)
        """
        return self.left < val < self.right


    def __neg__(self):
        """
        Switches interval enpoints and changes the sign of them.

        returns _ : Interval (New interval after switching sign and
                              place of endpoints.)
        """
        return Interval(self.right * -1, self.left * -1)

    # |------------------------------ Task 6 ------------------------------|#
    # See at specified part of code

    # |------------------------------ Task 7 ------------------------------|#
    # See at specified part of code

    # |------------------------------ Task 8 ------------------------------|#
    # Didn't bother to make a shell script (too much work, just run the
    # check_task_8() function)

    # |------------------------------ Task 9 ------------------------------|#

    def __pow__(self, p):
        """
        Computes the interval with endpoints to the power if p.

        parameter p : int, float (Number to raise to the power of)
        returns _ : Interval (With enpoints raised to the power of p)
        """

        a, b = self.left, self.right

        # If p is less than zero raise value error.
        if p < 0:
            raise ValueError(
                f"""Exponential operation not defined for {p}.
                \n Please make sure p is not less than zero."""
            )

        # Even case
        if p % 2 == 0:
            if a >= 0:
                return Interval(a ** p, b ** p)
            elif b < 0:
                return Interval(b ** p, a ** p)
            else:
                return Interval(0, max(a ** p, b ** p))

        # Odd case
        return Interval(a ** p, b ** p)


# |------------------------------ Task 10 ------------------------------|#


def task_10():
    """Solution to task 10"""

    xl = linspace(0.0, 1, 1000)
    xu = linspace(0.0, 1, 1000) + 0.5

    # Creates list of 1000 intervals with lower enpoint from xl and
    # upper endpoint from xu.
    intervals = [Interval(l, u) for l, u in zip(xl, xu)]

    # Polynomial function to evaluate on intervals
    pol = lambda I: 3 * I ** 3 - 2 * I ** 2 - 5 * I - 1

    # Extract a list of lower boundaries yl and upper boundaries yu
    evaluated_intervals = [pol(I) for I in intervals]
    yl = [I.left for I in evaluated_intervals]
    yu = [I.right for I in evaluated_intervals]

    # Plot graphs versus xl
    figure(0)
    plot(xl, yu, label="upper")
    plot(xl, yl, label="lower")
    xlabel(r"$x$")
    ylabel(r"$p(I)$")
    title(r"$p(I)=3I^3-2*I^2-5*I-1$, I $=$ Interval$(x, x + 0.5)$")
    legend()
    show()


def check_task_3():
    """
    Validates the result of task 3.
    """

    print("\nChecking task 3...\n")
    print(f"Interval(1, 2) \t \t is {Interval(1, 2)} and should equal [1, 2].\n")


def check_task_4():
    """
    Validates the result of task 4.
    """

    I1 = Interval(1, 4)
    I2 = Interval(-2, -1)

    print("\nChecking task 4...\n")
    print(f"I1 = Interval(1, 4) \t is {I1} and should equal [1, 4].")
    print(f"I2 = Interval(-2, -1) \t is {I2} and should equal [-2, -1].")
    print(f"I1 + I2 \t \t is {I1 + I2} and should equal [-1, 3].")
    print(f"I1 - I2 \t \t is {I1 - I2} and should equal [2, 6].")
    print(f"I1 * I2 \t \t is {I1 * I2} and should equal [-8, -1].")
    print(f"I1 / I2 \t \t is {I1 / I2} and should equal [-4.,-0.5].\n")


def check_task_8():
    """
    Validates the result of task 8.
    """

    I = Interval(2, 3)

    print("\nChecking task 8...\n")
    print(f"Interval(2,3) + 1 \t is {I + 1} and should equal [3, 4].")
    print(f"1 + Interval(2,3) \t is {1 + I} and should equal [3, 4].")
    print(f"1.0 + Interval(2,3) \t is {1.0 + I} and should equal [3.0, 4.0].")
    print(f"Interval(2,3) + 1.0 \t is {I + 1.0} and should equal [3.0, 4.0].")

    print(f"1 - Interval(2,3) \t is {1 - I} and should equal [-2, -1].")
    print(f"Interval(2,3) - 1 \t is {I - 1} and should equal [1, 2].")
    print(f"1.0 - Interval(2,3) \t is {1.0 - I} and should equal [-2.0, -1.0].")
    print(f"Interval(2,3) - 1.0 \t is {I - 1.0} and should equal [1.0, 2.0].")

    print(f"Interval(2,3) * 1 \t is {I * 1} and should equal [2, 3].")
    print(f"1 * Interval(2,3) \t is {1 * I} and should equal [2, 3].")
    print(f"1.0 * Interval(2,3) \t is {1.0 * I} and should equal [2.0, 3.0].")
    print(f"Interval(2,3) * 1.0 \t is {I * 1.0} and should equal [2.0, 3.0].")

    print(f"-Interval(2,3) \t \t is {-I} and should equal [-3, -2].\n")


def check_task_9():
    """
    Validates the result of task 9.
    """

    x = Interval(-2, 2)

    print("\nChecking task 9...\n")
    print(f"x**2 is {x**2}, should be [0, 4]")
    print(f"x**3 is {x**3}, should be [-8, 8]\n")


if __name__ == "__main__":
    main()
