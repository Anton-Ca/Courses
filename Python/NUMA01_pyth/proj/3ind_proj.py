#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The purpose is to provide a solution to the birds final project
in the course numa01 Computational Programming with Python,
Summer 2022. The goal is to gather expertise programming in
group and the task at hand consists of processing and analysing
a large data set.

@Author: Anton Carlsson, Natalia Timokhova, Harald Toft, Weikang Ke
"""


from os.path import dirname, join
from re import sub
from datetime import datetime, timedelta
from pytz import timezone
#from matplotlib.pyplot import *


FILENAME = join(
    dirname(__file__), "bird_jan25jan16.txt"
)  # Assumes file in current folder


def main():
    """Main function of the program."""
    dates, counts = read_data()
    dates, counts = pre_process(dates, counts)
    print(
        "\nCurrent timezone is set to UTC",
        dates[0].astimezone(tz=timezone('UTC')).isoformat()[-6:-3],
        " Coordinated Universal Time.\n",
        sep="",
    )

    # prepare_to_plot(dates, counts)            # TODO: Implement this
    # plot_stuff(dates, counts)                 # TODO: Implement this
    # day_and_night(dates, counts)              # TODO: Implement this
    # Make sure all questions are answered
    # Think about whether we can speed up
    # some of the code and make it run faster
    # additional_improvements(dates, counts)    # TODO: Implement this


def read_data():
    """
    Takes in a string filename and reads the data of the corresponding file.
    Outputs dates and counts all as list objects containing the data found
    in the input data file.

    :param filename: str (Name of file to read)
    :return dates, counts: *list (Lists for all dates and counts)
    """

    dates = []
    counts = []

    with open(FILENAME, "r") as data:
        for line in data:

            # Switch all white whitespace characters to a single space " "
            line = sub(r"[\s]+", " ", line)
            # Separate the data based on spaces and exclude last empty element
            line = line.split(" ")[:-1]

            # Datetime objects containing date & time, where timezone is set to UTC
            # .fromisoformat() is almost 50x faster than .strptime() and
            # documentation can be found here:
            # https://docs.python.org/3/library/datetime.html#:~:text=classmethod%20datetime.-,fromisoformat,-(date_string)
            dates.append(
                datetime.fromisoformat(join(line[0], line[1])).astimezone(
                    tz=timezone("UTC")
                )
            )
            counts.append(int(line[2]))

    return dates, counts


def pre_process(dates, counts):
    """
    Takes in dates and counts as list objects and processes the list in order
    to handle inaccurate data.

    :param dates, counts : list (Lists for all dates and counts)
    :return dates, counts : type (Processed data)
    """

    counts = fix_incomplete_counts(counts)  # Perhaps this can be used to solve fix_bio_err?
    print()
    print(len(dates))
    print()
    dates, counts = fix_missing_lines(dates, counts)
    print()
    print(len(dates))
    print()
    dates, counts = fix_bio_err(dates, counts)
    print()
    print(len(dates))
    print()

    # Think about making the functions here used internal (could be prettier)

    return dates, counts


def fix_incomplete_counts(counts):
    """
    Fixes data where the counts are reported inaccurately as in the third column
    second row below. The solution is to replace the count with the average of
    the surrounding data points.

    2015-03-01  14:20:06.911302  2072
    2015-03-01  14:22:05.911302  72
    2015-03-01  14:24:08.911302  2072

    :param dates: list (Lists for all counts)
    :return counts : list (Processed counts)
    """
    for ind in range(1, len(counts) - 1):
        before = counts[ind - 1]
        current = counts[ind]
        after = counts[ind + 1]
        if current < before and current < after:
            counts[ind] = int((before + after) / 2)

    return counts


def fix_missing_lines(dates, counts):
    """
    Fixes data where there are some entire lines missing.
    The solution is to take the average of the previous and next count
    and insert new rows for every two minutes that are missing.
    Example:

    2015-03-01  14:12:06.911302  X
    2015-03-01  14:ZZ:05.911302  (X + Y) / 2      # Should be same as X
    2015-03-01  14:28:08.911302  Y

    Above ZZ in the middle row is every two minute from 12 to 28.

    :param dates counts: *list (Lists for all counts)
    :return dates, counts : *list (Processed counts)
    """

    time_step = 2
    last_date = dates[-1]
    for _ in range(0,1):
        added = 0
        add = []
        print(10*"\n", "Starting loop "*5, 10*"\n")
        # We want the index from enumerate, so prefer this over while
        for ind, _ in enumerate(dates):       # ind, is same as ind, _
            real_ind = ind

            # Break loop if we reach end (to avoid IndexError)
            if dates[real_ind] == last_date:
                break

            current_date, current_count = (dates[real_ind], counts[real_ind])
            next_date, next_count = (dates[real_ind + 1], counts[real_ind + 1])

            # If difference in minutes exceeds 4 we can insert new row
            if abs((current_date - next_date).total_seconds()) >= 240:
                # Previous date +2 minutes (formatting with hours etc automatic)
                new_date = current_date + timedelta(minutes=time_step)
                # What happends if it's a very large gap where the counts can differ
                # a lot before and after? Case we need to handle?
                new_count = int((current_count + next_count) / 2)

                # Insert new row after the element real_ind in dates and counts
                #dates[real_ind: real_ind] = [new_date]
                #counts[real_ind: real_ind] = [new_count]
                # This should effectively fill upp all gaps no mater how many
                # rows are missing.

                #print(current_date, next_date, sep="\t")
                #print(3*"\t",  abs(((current_date - next_date).total_seconds())))

                # Increment counter for how many elements we added to keep track of lists
                added += 1

                add.append(real_ind)

        for i, d in enumerate(dates):
            if i in add:
                dates = dates[:i] + [(dates[i] + timedelta(seconds=j)) for j in range(0, int(abs((dates[i]-dates[i+1])).total_seconds()), time_step*60)] + dates[i+1:]


    return dates, counts


def fix_bio_err(dates, counts):
    """
    Fixes data where there are multiple additional counts.
    The solution cosists of finding rows that are less than
    fifteen seconds apart and removing lines until there are
    no such matches.
    Example:

    2015-03-01  14:12:06.911302  X      # Delete this line
    2015-03-01  14:12:10.911302  X
    2015-03-01  14:15:08.911302  X

    :param dates counts: *list (Lists for all counts)
    :return dates, counts : *list (Processed counts)
    """

    time_step = 2
    last_date = dates[-1]
    for _ in range(0,1):
        remove = []
        print(10*"\n", "Starting loop "*5, 10*"\n")
        # We want the index from enumerate, so prefer this over while
        for ind, _ in enumerate(dates):       # ind, is same as ind, _
            real_ind = ind

            # Break loop if we reach end (to avoid IndexError)
            if dates[real_ind] == last_date:
                break

            current_date, current_count = (dates[real_ind], counts[real_ind])
            next_date, next_count = (dates[real_ind + 1], counts[real_ind + 1])

            # 4 per minute 60/4=15 seconds
            if abs((current_date - next_date).total_seconds()) < 15:
                remove.append(real_ind)

        if remove != []:
            dates = [d for (i, d) in enumerate(dates) if i not in remove]
            counts = [c for (i, c) in enumerate(counts) if i not in remove]
            print(f"\nNumber removed elements: {len(remove)}",
                    f"Last removed index: {remove[-1]}\n")

    return dates, counts


if __name__ == "__main__":
    main()
