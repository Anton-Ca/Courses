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
import numpy as np
import pandas as pd
from re import sub
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pytz import timezone


FILENAME = join(
    dirname(__file__), "bird_jan25jan16.txt"
)  # Assumes file in current folder


def main():
    """Main function of the program."""
    #dates, counts = read_data()
    #dates, counts = pre_process(dates, counts)
#    print(
#        "\nCurrent timezone is set to UTC",
#        dates[0].astimezone(tz=timezone('UTC')).isoformat()[-6:-3],
#        " Coordinated Universal Time.\n",
#        sep="",
#    )


    dates, counts = read_data()

    newDates = dateTimeFormat(dates)
    zipList = list(zip(newDates, counts))
    birdPd = pd.DataFrame(zipList, columns=['DateTime', 'Count']) #convert to pandas

    ##debug
    print("Shape unprocessed", birdPd.shape[0])
    birdPd = fix_incomplete_counts(birdPd)
    print("Shape remove weird", birdPd.shape[0])
    birdPd = fixMissingLine(birdPd)
    print("Shape fixed missing date1", birdPd.shape[0])
    birdPd = datePerMinute(birdPd)
    print("Shape datePerMinute", birdPd.shape[0]) # why two index less
    birdPd = limitMotion(birdPd)
    print("Shape limit Motion", birdPd.shape[0])
    ax1 = birdPd.loc[1:238748,'Count'].plot()

    #plotTEST
    birdPd.set_index('DateTime', drop=True, inplace=True)
    birdPd.loc['2015-01-25 13:10']
    birdPd.loc['2016-01-16 16:14']
    ax2 = birdPd.loc['2015-01-25 13:10':'2015-02-16 16:14'].plot()
    plt.show()

    # prepare_to_plot(dates, counts)            # TODO: Implement this
    # plot_stuff(dates, counts)                 # TODO: Implement this
    # day_and_night(dates, counts)              # TODO: Implement this
    # Make sure all questions are answered
    # Think about whether we can speed up
    # some of the code and make it run faster
    # additional_improvements(dates, counts)    # TODO: Implement this



def read_data():
    """
    read csv into datetime objects, and counts
    """
    dates = []
    counts = []
    with open(FILENAME, "r") as data:
        for line in data:

            # Switch white whitespace characters single space " "
            line = sub(r"[\s]+", " ", line)
            # Separate the data based on spaces and exclude last empty element ##why??
            line = line.split(" ")[:-1]
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
    return dates, counts


# convert
# Unused
#def convertToPdTimeStamp(dates):
#    """
#    convert datetime obj to pd timestamp obj **UNUSED**
#
#    """
#
#    for i in range(len(dates)):
#        dates[i]=pd.Timestamp(year = dates[i].year ,
#                              month = dates[i].month,
#                              day = dates[i].day,
#                              hour = dates[i].hour,
#                              minute = dates[i].minute,
#                              tz = 'UTC')
#    return dates


# TODO:
# Why is this function necessary? - It's not but for our sake :)
# We can use isoformat func instead :)
def dateTimeFormat(dates, dateForm='%Y-%m-%d %H:%M'):
    """ reformat datetime """
    return [datetime.strptime(date.strftime(dateForm), dateForm) for date in dates]
    #for i in range(len(dates)):
    #    dates[i] = dates[i].strftime(dateForm)
    #    dates[i] = datetime.strptime(dates[i], dateForm)
    #return(dates)


# address reset (NOT FUNCTIONAL)
# Unused
#def resetFix(birdPd):
#    for i in range(birdPd.shape[0]-1):
#        if birdPd.loc[i].at["DateTime"].minute < birdPd.loc[i+1].at["DateTime"].minute:
#            birdPd.drop(birdPd.loc[i], axis=0)
#            #for i in range()
#            birdPd.loc[i+1].at["Count"] = birdPd.loc[i+1].at["Count"] + birdPd.loc[i].at["Count"]

#|------------------------------ Pre Processing ------------------------------|#

def fix_incomplete_counts(bird_counts):
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

    for ind in range(1, bird_counts.shape[0]-1):
        before = bird_counts.loc[ind-1, "Count"]
        current = bird_counts.loc[ind, "Count"]
        after = bird_counts.loc[ind+1, "Count"]
        if current < before and current < after:
            bird_counts.loc[ind, "Count"] = int((before+after)/2)

    return bird_counts


# Unused
#def fix_missing_lines2(birdPd, sen=2):
#    """
#    Fixes data where there are some entire lines missing.
#    The solution is to take the average of the previous and next count
#    and insert new rows for every two minutes that are missing.
#    Example:
#
#    2015-03-01  14:12:06.911302  X
#    2015-03-01  14:ZZ:05.911302  (X + Y) / 2      # Should be same as X
#    2015-03-01  14:28:08.911302  Y
#
#    Above ZZ in the middle row is every two minute from 12 to 28.
#
#    :param dates counts: *list (Lists for all counts)
#    :return dates, counts : *list (Processed counts)
#    """
#
#    for i in range(1, birdPd.shape[0]-sen*2):
#        avgBefore = np.mean(birdPd.loc[i-sen:i, "Count"])
#        current = birdPd.loc[i, "Count"]
#        avgAfter = np.mean(birdPd.loc[i+1:i+sen+1, "Count"])
#        if current < avgBefore and current < avgAfter:
#            birdPd.loc[i, "Count"] = int((avgBefore+avgAfter)/2)
#    return birdPd


##2
def fixMissingLine(birdPd):
    """
    For missing minutes, it puts a time in between with the same count

    For all normal lines it puts the pandas content into a new list.
    For missing minutes it creates a new line with mean minutes with same count.
    And the they are appended to the new list
    Lastly, the list is converted to pandas

    """
    newBird = []
    for ind in range(0, birdPd.shape[0]-1):
        if birdPd.loc[ind+1,"DateTime"].minute - birdPd.loc[ind,"DateTime"].minute <= 2 :
            newBird.append([birdPd.loc[ind,"DateTime"],birdPd.loc[ind,"Count"]])
        elif birdPd.loc[ind+1,"DateTime"].minute - birdPd.loc[ind,"DateTime"].minute > 2 :
            gapMin = (birdPd.loc[ind,"DateTime"].minute + birdPd.loc[ind+1,"DateTime"].minute) / 2
            #newTime = datetime(year = birdPd.loc[ind,"DateTime"].year,
            #                            month = birdPd.loc[ind,"DateTime"].month,
            #                            day = birdPd.loc[ind,"DateTime"].day,
            #                            hour = birdPd.loc[ind,"DateTime"].hour,
            #                            minute = int(gapMin))
            #temp = [newTime, birdPd.loc[ind,"Count"]]
            # TODO:
            # Why not use timedelta()? - We can :)
            # Fix hardcoded numbers such as 2 eg. rename to time_step
            temp = [birdPd.loc[ind, "DateTime"] + timedelta(minutes=2), birdPd.loc[ind,"Count"]]
            #print("Missing minute fixed")
            newBird.append(temp)
    newBird.append([birdPd.iloc[-1].at["DateTime"],birdPd.iloc[-1].at["Count"]]) #last data
    newBirdPd = pd.DataFrame(newBird, columns=['DateTime', 'Count'])
    return newBirdPd


##3
def datePerMinute(birdPd):
    """
    #Reduce to data per minute first
    """
    dateList = []
    for i in range(birdPd.shape[0]):
        temp = [birdPd.loc[i,'DateTime'].year,
                birdPd.loc[i,'DateTime'].month,
                birdPd.loc[i,'DateTime'].day,
                birdPd.loc[i,'DateTime'].hour,
                birdPd.loc[i,'DateTime'].minute,
                birdPd.loc[i,'DateTime']]
        dateList.append(temp)
    print()
    print(birdPd.loc[0,'DateTime'])
    print()
    datePd = pd.DataFrame(dateList, columns=['year',
                                             'month',
                                             'day',
                                             'hour',
                                             'minute',
                                             'DateTime'])

    print(datePd.iloc[0])
    print()
    birdExtend = pd.merge(datePd, birdPd, on='DateTime')
    print('\t', birdExtend.loc[0,'DateTime'], sep='')
    print()
    #birdPd.set_index('DateTime', drop=True, inplace=True)
    birdMinutes = birdExtend.groupby(['year',
                                      'month',
                                      'day',
                                      'hour',
                                      'minute'],
                                     as_index=False).agg({'Count':'mean',
                                                      'DateTime':'mean'})
    print(birdMinutes.iloc[0])
    print()
    return(birdMinutes)

def limitMotion(birdPd):
    for i in range(0, birdPd.shape[0]-1):
        minute = birdPd.iloc[i+1].at["DateTime"].minute - birdPd.iloc[i].at["DateTime"].minute
        move = birdPd.iloc[i+1].at["Count"] - birdPd.iloc[i].at["Count"]
        #print(move)
        if move > 0 :
            mPm = minute/move
            if mPm > 4 :
                moveCorrect = 4*minute
                birdPd.loc[i+1,"Count"]=birdPd.loc[i,"Count"] + moveCorrect
    return birdPd


if __name__ == "__main__":
    main()
