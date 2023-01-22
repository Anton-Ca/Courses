#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 19:05:53 2022

@author: supamafia
"""

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

#import
def read_data():
    """
    read csv into datetime objects, and counts
    """
    dates = []
    counts = []
    with open('bird_jan25jan16.txt', "r") as data:
        for line in data:

            line = sub(r"[\s]+", " ", line) # Switch white whitespace characters single space " "
            line = line.split(" ")[:-1] # Separate the data based on spaces and exclude last empty element ##why??
            tempList=list(np.zeros(2)) #empty list
            tempList[0]=line[0]
            tempList[1]=line[1]
            temp=" ".join(tempList) #join the first two part
            dates.append(
                datetime.fromisoformat(temp).astimezone(
                    tz = timezone("UTC")
                )
            ) # Datetime objects containing date & time, where timezone is set to UTC
            counts.append(int(line[2]))
    return (dates,counts)

# convert
"""
def convertToPdTimeStamp(dates):

    #convert datetime obj to pd timestamp obj **UNUSED**

    for i in range(len(dates)):
        dates[i]=pd.Timestamp(year = dates[i].year ,
                              month = dates[i].month,
                              day = dates[i].day,
                              hour = dates[i].hour,
                              minute = dates[i].minute,
                              tz = 'UTC')
    return dates

"""

def dateTimeFormat(dates, dateForm='%Y-%m-%d %H:%M'):

    # reformat datetime


    for i in range(len(dates)):
        dates[i] = dates[i].strftime(dateForm)
        dates[i] = datetime.strptime(dates[i], dateForm)
    return(dates)

##pre processing

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

    for ind in range(1, bird_data.shape[0]-1):
        before = bird_data.loc[ind-1, "Count"]
        current = bird_data.loc[ind, "Count"]
        after = bird_data.loc[ind+1, "Count"]
        if current < before and before <= after:
            bird_data.loc[ind, "Count"] = int((before+after)/2)

    return bird_data


def fixMissingLine(birdPd):
    """
    For missing minutes, it puts a time in between with the same count
    For all normal lines it puts the pandas content into a new list.
    For missing minutes it creates a new line with mean minutes with same count.
    And the they are appended to the new list
    Lastly, the list is converted to pandas
    """

    newBird = []
    for i in tqdm(range(0, birdPd.shape[0]-1)):
        diff = int((birdPd.loc[i+1,"DateTime"] - birdPd.loc[i,"DateTime"]).seconds/60)
        if abs(diff) < 1.9:
            print("Error!")
        if diff < 0:
            birdPd.drop([i], axis=0, inplace =True)
            continue
        if diff <= 2 :
            newBird.append([birdPd.loc[i,"DateTime"],birdPd.loc[i,"Count"]])
        else:
            real_diff = diff/2
            nbr_missing_lines = diff//2
            newBird.append([birdPd.loc[i,"DateTime"],birdPd.loc[i,"Count"]])
            if real_diff <= nbr_missing_lines:
                for order in range(1, nbr_missing_lines):
                    temp = [birdPd.loc[i, "DateTime"] + timedelta(minutes = order * 2), birdPd.loc[i,"Count"]]
                    newBird.append(temp)
            if real_diff > nbr_missing_lines:
                for order in range(1, nbr_missing_lines + 1):
                    temp = [birdPd.loc[i, "DateTime"] + timedelta(minutes = order * 2), birdPd.loc[i,"Count"]]
                    newBird.append(temp)
            newBird.append([birdPd.loc[i+1,"DateTime"],birdPd.loc[i,"Count"]])
    newBird.append([birdPd.iloc[-1].at["DateTime"], birdPd.iloc[-1].at["Count"]]) #last data
    newBirdPd = pd.DataFrame(newBird, columns=['DateTime', 'Count'])
    return newBirdPd


def resetFix(birdPd):
    s=0
    for i in tqdm( range(1,birdPd.shape[0])):
        if birdPd.loc[i, "Count"] < birdPd.loc[i-1, "Count"] :
            birdPd.loc[i:,'Count']+=(birdPd.loc[i-1, 'Count']-s)
            s=birdPd.loc[i-1, 'Count']
    return birdPd


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
    totalerror = 0
    for ind in tqdm(range(1, data_size-1)):

        next_count = int(bird_data.loc[ind+1, "Count"]) - totalerror
        bird_data.loc[ind+1, "Count"] = next_count
        current_count = int(bird_data.loc[ind, "Count"])

        date_one = bird_data.loc[ind+1, "DateTime"]
        date_two = bird_data.loc[ind, "DateTime"]
        maximum_next = current_count + 8
        countdiff = next_count - current_count

        #if ind == 1220:
        #    print("error here")

        if countdiff > 8:
            bird_data.loc[ind+1, "Count"] = maximum_next
            error = next_count - maximum_next
            totalerror += error

    return bird_data


# run pre processing

def runPre():
    dates = read_data()[0] # get dates List
    newDates = dateTimeFormat(dates)
    counts = [float(x) for x in (read_data()[1])] #get counts List
    zipList = list(zip(newDates, counts)) #zip two lists
    birdPd = pd.DataFrame(zipList, columns=['DateTime', 'Count']) #convert to pandas

    print(birdPd.shape[0])
    birdPd = fix_incomplete_counts(birdPd)
    print(birdPd.shape[0])
    birdPd = fixMissingLine(birdPd)
    #birdPd = fixMissingLine(birdPd)
    print(birdPd.shape[0])
    #checkMinuteGap(birdPd)
    birdPd = resetFix(birdPd)
    print(birdPd.shape[0])
    birdPd = limit_motions_per_min(birdPd)
    print(birdPd.shape[0])
    return birdPd

#birdPd = runPre(birdPd)

# plot
#ax1 = birdPd.loc[:, 'Count'].plot()
#plt.show()

#debug
def control_data(bird_data):
    """
    Controls that count difference is four

    2015-01-31 06:58:05.497286    268
    2015-01-31 07:00:05.993205    281   + (268 - 281) + (4 * 2)
    2015-01-31 07:02:05.306633    281   + (268 - 281) + (4 * 2)

    @param bird_data: pandas dataframe (Contains data)
    """
    data_size = bird_data.shape[0]
    for ind in tqdm(range(1,data_size-1)):
        current = int(bird_data.iloc[ind].at["Count"])
        next_value = int(bird_data.iloc[ind+1].at["Count"])
        diff = next_value - current
        if diff > 8:
            print(ind, diff)
            #raise ValueError("Difference between counts is too big index: ", ind)

def checkMinteGap(birdPd):
    for i in range(birdPd.shape[0]-1):
        diff_minutes = (birdPd.loc[i+1, 'DateTime']- birdPd.loc[i, 'DateTime']).seconds/60
        if diff_minutes > 2 :
            print (diff_minutes, i)


