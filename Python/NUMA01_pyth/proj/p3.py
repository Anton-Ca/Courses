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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pytz import timezone
from tqdm import tqdm


# Global constant
FILENAME = join(
    dirname(__file__), "bird_jan25jan16.txt"
)


def main():
    """Main function of the program."""

    load_from_pickle = True      # False if we want to run normally
    bird_data = None
    if not load_from_pickle:     # We skip these if we have a bird_data to just load instead
        dates, counts = read_data()
        new_dates = date_time_format(dates)
        zip_list = list(zip(new_dates, counts))
        bird_data = pd.DataFrame(zip_list, columns=['DateTime', 'Count']) #convert to pandas

    bird_data = pre_process(bird_data, load_from_pickle)

    # Plot some stuff
    #plt.figure(1)
    #ax1 = bird_data.loc[1:238748,'Count'].plot()   # Unused?
    #bird_data.set_index('DateTime', drop=True, inplace=True)
    #ax2 = bird_data.loc['2015-01-25 13:10':'2015-02-16 16:14'].plot() # Unused?
    #plt.show()


def read_data():
    """
    Reads the data of the global file FILENAME and outputs dates
    and counts both as list objects containing the data found in
    the input data file.

    @return dates, counts: pandas dataframes (Pandas dataframes for all dates and counts)
    """

    dates = []
    counts = []
    with open(FILENAME, "r") as data:
        for line in data:

            # Switch white whitespace characters single space " "
            line = sub(r"[\s]+", " ", line)
            # Separate the data based on spaces and exclude last empty element ##why??
            line = line.split(" ")[:-1]
            temp_list=list(np.zeros(2)) #empty list
            temp_list[0] = line[0]
            temp_list[1] = line[1]
            temp = " ".join(temp_list) #join the first two part
            dates.append(
                datetime.fromisoformat(temp).astimezone(
                    tz = timezone("UTC")
                )
            ) # Datetime objects containing date & time, where timezone is set to UTC
            counts.append(int(line[2]))
    return dates, counts


# TODO:
# We can use isoformat func instead :)
def date_time_format(dates, date_format='%Y-%m-%d %H:%M'):
    """
    Reformats the dates into the format specified py the date_format parameter.

    @param dates: list (Containing all dates)
    @param date_format: str (Corresponding to desired date format)
    @return dates: list (Reformatted list of all dates)
    """

    return [datetime.strptime(date.strftime(date_format), date_format) for date in dates]


#|------------------------------ Pre Processing ------------------------------|#


def pre_process(bird_data, load_from_pickle=False):
    """
    Takes in dates and counts as pandas dataframe objects and performs
    preprocessing in order to deal with inaccurate data.

    @param bird_data: pandas dataframe (Contains all dates and counts)
    @return bird_data: pandas dataframe (Processed dates and counts)
    """

    if not load_from_pickle:
        #print("Shape unprocessed", bird_data.shape[0])
        #bird_data = bird_data.iloc[1:238748//25]       # Uncomment to speed up
        bird_data = fix_incomplete_counts(bird_data)
        #print("Shape remove weird", bird_data.shape[0])
        bird_data = fix_missing_lines(bird_data)
        #print("Shape reset Fix", bird_data.shape[0])
        bird_data = fix_reset(bird_data)

        if bird_data.shape[0] > 238748//5:
            bird_data.to_pickle('bird_data.pkl')
        # Place this below limit_motions_per_min(bird_data) if you want to
        # skip waiting for this function as well

        #print("Shape datePerMinute", bird_data.shape[0]) # why two index less
        bird_data = limit_motions_per_min(bird_data)
        #print("Shape limit Motion", bird_data.shape[0])
    else:
        bird_data = pd.read_pickle('bird_data.pkl')
        # Place this below limit_motions_per_min(bird_data) if you want to
        # skip waiting for this function as well
        bird_data = bird_data.iloc[1:238748//25]       # Uncomment to speed up

        # Debug
        #for ind in range(0, bird_data.shape[0]-1):
        #    print_counts = False
        #    if print_counts:
        #        nextt = bird_data.iloc[ind+1].at["Count"]
        #        current = bird_data.iloc[ind].at["Count"]
        #        diff = (nextt - current)
        #    else:
        #        nextt = bird_data.iloc[ind+1].at["DateTime"]
        #        current = bird_data.iloc[ind].at["DateTime"]
        #        diff = (nextt - current).total_seconds()
        #    if diff < 0:
        #       print(current)
        #       print(nextt, "\n")

        bird_data = limit_motions_per_min(bird_data)

        # CHANGE HERE IF YOU DON'T WANT TO PLOT DURING TESTING
        plt.figure(0)
        ax1 = bird_data.loc[1:bird_data.shape[0],'Count'].plot()   # Unused?
        bird_data.set_index('DateTime', drop=True, inplace=True)
        plt.show()

    # Think about making the functions here used internal (could be prettier)
    return bird_data


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

    for ind in range(2, bird_data.shape[0]-1):
        before = bird_data.loc[ind-1, "Count"]
        current = bird_data.loc[ind, "Count"]
        after = bird_data.loc[ind+1, "Count"]
        if current < before <= after:
            bird_data.loc[ind, "Count"] = int((before+after)/2)

    return bird_data


##2
def fix_missing_lines(bird_data):
    """
    Fixes data where there are some entire lines missing.
    The solution and insert new rows for every two minutes
    that are missing. Example:

    2015-03-01  14:12:06.911302  X
    2015-03-01  14:ZZ:05.911302  X      (Create these lines)
    2015-03-01  14:28:08.911302  Y

    Above ZZ in the middle row is every two minute from 12 to 28.

    @param bird_data: pandas dataframe (Contains data)
    @return bird_data : pandas dataframe (Contains data)
    """
    new_bird = []
    for ind in range(1, bird_data.shape[0]-1):
        diff = int((bird_data.loc[ind+1,"DateTime"] - bird_data.loc[ind,"DateTime"]).total_seconds()/60)
        if diff < 0:
            bird_data.drop([ind], axis=0, inplace =True)
            continue
        if diff <= 2:
            new_bird.append([bird_data.loc[ind,"DateTime"], bird_data.loc[ind,"Count"]])
        elif diff > 2:
            nbr_missing_lines = diff//2
            for order in range(1, nbr_missing_lines):
                temp = [bird_data.loc[ind, "DateTime"] + timedelta(minutes=2*order), bird_data.loc[ind,"Count"]]
                new_bird.append(temp)
    new_bird.append([bird_data.iloc[-1].at["DateTime"], bird_data.iloc[-1].at["Count"]]) #last data
    new_bird_data = pd.DataFrame(new_bird, columns=['DateTime', 'Count'])
    return new_bird_data


def fix_reset(bird_data):
    """
    Fixes errors in data where the counts resets to a lower number.
    The solution is to remove the lines with resets and to increase
    the count of following lines with the line prior to the reset.
    Example:

    2015-03-01  14:12:06.911302  200
    2015-03-01  14:10:05.911302  0      (Fix this line)
    2015-03-01  14:16:08.911302  2      + 200

    @param bird_data: pandas dataframe (Contains data)
    @return bird_data : pandas dataframe (Contains data)
    """

    data_size = bird_data.shape[0]
    for ind in range(2, data_size - 2):
        ind2 = 0
        current_count = bird_data.loc[ind].at["Count"]
        previous_count = bird_data.loc[ind-1].at["Count"]
        next_count = bird_data.loc[ind+1].at["Count"]

        if current_count < previous_count and next_count < previous_count:
            ind2=ind
            new_current_count = bird_data.loc[ind2].at["Count"]
            new_next_count = bird_data.loc[ind2+1].at["Count"]

            while new_current_count <= new_next_count and ind2 < (data_size - 1):
                bird_data.loc[ind2, "Count"] = new_current_count + previous_count
                ind2 += 1

            bird_data.loc[ind2, "Count"] = new_current_count + previous_count
            ind = ind2
    return bird_data


def limit_motions_per_min(bird_data):
    """
    Fixes data where there are multiple additional counts. The solution
    cosists finding intervals where counts exceeds the limit of 4 per
    minute and increase the following counts with the maximum allowed
    count times the amounts of minutes in the interval. Example:

    2015-01-31 06:58:05.497286    268
    2015-01-31 07:00:05.993205    281   + (268 - 281) + (4 * 2)
    2015-01-31 07:02:05.306633    281   + (268 - 281) + (4 * 2)

    @param bird_data: pandas dataframe (Contains data)
    @return bird_data : pandas dataframe (Contains data)
    """
    data_size = bird_data.shape[0]
    adjustment = 0
    for ind in tqdm(range(1, data_size-1)):
        #if ind > data_size - 4 or ind == 1000 or ind == 5000 or ind == 10000:
            #print(bird_data.loc[ind])
            #print(bird_data.loc[ind+1])
            #print(bird_data.loc[ind+1,"Count"])
        #    pass
        bird_data.loc[ind+1,"Count"] = bird_data.loc[ind+1,"Count"] + adjustment
        #if ind > data_size - 4 or ind == 1000 or ind == 5000 or ind == 10000:
            #print(bird_data.loc[ind+1,"Count"], "\n", sep="")
        #    pass

        next_count = bird_data.iloc[ind+1].at["Count"]
        current_count = bird_data.iloc[ind].at["Count"]

        diff_counts = (next_count - current_count)
        diff_dates = int(abs(bird_data.loc[ind+1,"DateTime"] - bird_data.loc[ind,"DateTime"]).total_seconds()/60)

        if diff_counts > 0:
            if (diff_counts / diff_dates) > 4:
                #print(f"ind: {ind}")
                adjustment += 4 * diff_dates - diff_counts
                bird_data.loc[ind+1,"Count"] = bird_data.loc[ind+1,"Count"] + adjustment
                #print(adjustment)
                #print(diff_dates)
                #print(diff_counts)
                #print(adjustment, "\n", sep="")

    # TODO:
    # Fix so no negative values or overflow

    return bird_data


if __name__ == "__main__":
    main()
