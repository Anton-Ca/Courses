#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
The purpose is to provide a solution to the birds final project
in the course numa01 Computational Programming with Python,
Summer 2022. The goal is to gather expertise programming in
group and the task at hand consists of processing and analysing
a large data set.

@author: Anton Carlsson, Natalia Timokhova, Harald Toft, Weikang Ke
"
"""


from os.path import dirname, join
import numpy as np
import pandas as pd
from re import sub
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from datetime import *
from pytz import *
from tqdm import tqdm
import astral.sun as ast


def read_data():
    """
    Reads the data of the variable filename and outputs dates
    and counts both as list objects containing the data found in
    the input data file.

    @return dates, counts: pandas dataframes (Pandas dataframes for all dates and counts)
    """

    dates = []
    counts = []
    filename = join(dirname(__file__), "bird_jan25jan16.txt")

    with open(filename, "r") as data:
        for line in data:
            line = sub(r"[\s]+", " ", line)
            line = line.split(" ")[:-1]
            temp = join(line[0], line[1])
            dates.append(datetime.fromisoformat(temp).astimezone(tz=timezone("UTC")))
            counts.append(int(line[2]))
    return (dates, counts)


def dateTimeFormat(dates, dateForm="%Y-%m-%d %H:%M"):
    for i in range(len(dates)):
        dates[i] = dates[i].strftime(dateForm)
        dates[i] = datetime.strptime(dates[i], dateForm)
    return dates


def fix_incomplete_counts(bird_data):
    """
    Fixes data where the counts are reported inaccurately as in the third column
    second row below. The solution is to replace the count with the average of
    the surrounding data points.

    2015-03-01  14:20:06.911302  2072
    2015-03-01  14:22:05.911302  72         (Fix this line)
    2015-03-01  14:24:08.911302  2072

    @param bird_data: pandas dataframe (Contains data for all counts)
    @return bird_data : pandas dataframe (Contains data for all counts)
    """

    for ind in range(1, bird_data.shape[0] - 1):
        before = bird_data.loc[ind - 1, "Count"]
        current = bird_data.loc[ind, "Count"]
        after = bird_data.loc[ind + 1, "Count"]
        if current < before and before <= after:
            bird_data.loc[ind, "Count"] = int((before + after) / 2)

    return bird_data


def fix_missing_line(bird_data):
    """
    Fixes data where there are some entire lines missing.
    The solution and insert new rows for every two minutes
    that are missing. Example:

    2015-03-01  14:12:06.911302  X
    2015-03-01  14:ZZ:05.911302  X      (Create these lines)
    2015-03-01  14:28:08.911302  Y

    Above ZZ in the middle row is every two minute from 12 to 28. Also fixes the case where the following line has an earlier date and removes this line.

    @param bird_data: pandas dataframe (Contains data)
    @return bird_data : pandas dataframe (Contains data)
    """

    newBird = []
    for i in tqdm(range(0, bird_data.shape[0] - 1)):
        diff = int((bird_data.loc[i + 1, "DateTime"] - bird_data.loc[i, "DateTime"]).seconds / 60)
        if diff < 0:
            bird_data.drop([i], axis=0, inplace=True)
            continue
        if diff <= 2:
            newBird.append([bird_data.loc[i, "DateTime"], bird_data.loc[i, "Count"]])
        else:
            real_diff = diff / 2
            nbr_missing_lines = diff // 2
            newBird.append([bird_data.loc[i, "DateTime"], bird_data.loc[i, "Count"]])

            if real_diff <= nbr_missing_lines:
                for order in range(1, nbr_missing_lines):
                    temp = [
                        bird_data.loc[i, "DateTime"] + timedelta(minutes=order * 2),
                        bird_data.loc[i, "Count"],
                    ]
                    newBird.append(temp)
            if real_diff > nbr_missing_lines:
                for order in range(1, nbr_missing_lines + 1):
                    temp = [
                        bird_data.loc[i, "DateTime"] + timedelta(minutes=order * 2),
                        bird_data.loc[i, "Count"],
                    ]
                    newBird.append(temp)
            newBird.append(
                [bird_data.loc[i + 1, "DateTime"], bird_data.loc[i, "Count"]]
            )
    newBird.append(

        [bird_data.iloc[-1].at["DateTime"], bird_data.iloc[-1].at["Count"]]
    )  # last data
    newBirdPd = pd.DataFrame(newBird, columns=["DateTime", "Count"])

    return newBirdPd


def fix_reset(bird_data):
    s = 0
    for i in tqdm(range(1, bird_data.shape[0])):
        if bird_data.loc[i, "Count"] < bird_data.loc[i - 1, "Count"]:
            bird_data.loc[i:, "Count"] += bird_data.loc[i - 1, "Count"] - s
            s = bird_data.loc[i - 1, "Count"]
    return bird_data


def limit_motions_per_min(bird_data):
    """
    Fixes data where there are multiple additional counts. The solution
    consists in finding intervals where counts exceeds the limit of 4 per
    minute and increase the following counts with the maximum allowed
    count times the amounts of minutes in the interval. Example:

    2015-01-31 06:58:05.497286    268
    2015-01-31 07:00:05.993205    281   + (268 - 281) + (4 * 2)
    2015-01-31 07:02:05.306633    281   + (268 - 281) + (4 * 2)

    @param bird_data: pandas dataframe (Contains data)
    @return bird_data : pandas dataframe (Contains data)
    """

    data_size = bird_data.shape[0]
    total_error = 0
    for ind in tqdm(range(1, data_size - 1)):

        next_count = int(bird_data.loc[ind + 1, "Count"]) - total_error
        bird_data.loc[ind + 1, "Count"] = next_count
        current_count = int(bird_data.loc[ind, "Count"])

        date_one = bird_data.loc[ind + 1, "DateTime"]
        date_two = bird_data.loc[ind, "DateTime"]
        maximum_next = current_count + 8
        count_diff = next_count - current_count

        if count_diff > 8:
            bird_data.loc[ind + 1, "Count"] = maximum_next
            error = next_count - maximum_next
            total_error += error

    return bird_data


def run_pre_process():
    """
    Runs pre processing steps seperated into individual functions.

    @return bird_data: pandas dataframe (Processed dates and counts)
    """

    print("Reading dates")
    dates = read_data()[0]  # get dates List
    new_dates = dateTimeFormat(dates)
    counts = [float(x) for x in (read_data()[1])]  # get counts List
    zip_data = list(zip(new_dates, counts))  # zip two lists
    bird_data = pd.DataFrame(
        zip_data, columns=["DateTime", "Count"]
    )  # convert to pandas

    print("Fixing incomplete counts")
    bird_data = fix_incomplete_counts(bird_data)
    print("Fixing missing lines")
    bird_data = fix_missing_line(bird_data)
    print("Fixing resets")
    bird_data = fix_reset(bird_data)
    print("Limiting motions")
    bird_data = limit_motions_per_min(bird_data)

    return bird_data


def control_data(bird_data):
    """
    Controls that count difference is four

    2015-01-31 06:58:05.497286    268
    2015-01-31 07:00:05.993205    281   + (268 - 281) + (4 * 2)
    2015-01-31 07:02:05.306633    281   + (268 - 281) + (4 * 2)

    @param bird_data: pandas dataframe (Contains data)
    """
    data_size = bird_data.shape[0]
    for ind in tqdm(range(1, data_size - 1)):
        current = int(bird_data.iloc[ind].at["Count"])
        next_value = int(bird_data.iloc[ind + 1].at["Count"])
        diff = next_value - current
        if diff > 8:
            print(ind, diff)
            # raise ValueError("Difference between counts is too big index: ", ind)


def checkMinteGap(bird_data):
    for i in range(bird_data.shape[0] - 1):
        diff_minutes = (
            bird_data.loc[i + 1, "DateTime"] - bird_data.loc[i, "DateTime"]
        ).seconds / 60
        if diff_minutes > 2:
            print(diff_minutes, i)
