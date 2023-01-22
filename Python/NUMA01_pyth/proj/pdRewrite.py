#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 10:20:58 2022

@author: supamafia
"""

import numpy as np
import pandas as pd
from re import sub
import matplotlib.pyplot as plt
from datetime import *
from pytz import *

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

dates = read_data()[0] # get dates List

# convert
def convertToPdTimeStamp(dates):
    """
    convert datetime obj to pd timestamp obj **UNUSED**

    """
    
    for i in range(len(dates)):
        dates[i]=pd.Timestamp(year = dates[i].year ,
                              month = dates[i].month,
                              day = dates[i].day,
                              hour = dates[i].hour,
                              minute = dates[i].minute,
                              tz = 'UTC')
    return dates

def dateTimeFormat(dates, dateForm='%Y-%m-%d %H:%M'):
    """
    reformat datetime

    """
    for i in range(len(dates)):
        dates[i] = dates[i].strftime(dateForm)
        dates[i] = datetime.strptime(dates[i], dateForm)
    return(dates)

newDates = dateTimeFormat(dates)
counts = [float(x) for x in (read_data()[1])] #get counts List
zipList = list(zip(newDates, counts)) #zip two lists
birdPd = pd.DataFrame(zipList, columns=['DateTime', 'Count']) #convert to pandas


# address reset (NOT FUNCTIONAL)

def resetFix(birdPd):
    for i in range(birdPd.shape[0]-1):
        if birdPd.loc[i].at["DateTime"].minute < birdPd.loc[i+1].at["DateTime"].minute:
            birdPd.drop(birdPd.loc[i], axis=0)
            #for i in range()
            birdPd.loc[i+1].at["Count"] = birdPd.loc[i+1].at["Count"] + birdPd.loc[i].at["Count"]
            

#pre processing
##1 
def dropWeird(birdPd): 
    """
    For corrupted data, it takes on the average of its neighbors

    """
    for i in range(1, birdPd.shape[0]-2):
        before = birdPd.loc[i-1, "Count"]
        current = birdPd.loc[i, "Count"]
        after = birdPd.loc[i+1, "Count"]
        if current < before and current < after:
            birdPd.loc[i, "Count"] = int((before+after)/2)
    return birdPd

def dropWeird2(birdPd, sen=2): 
    """
    For corrupted data, it takes on the average of its n neighbors
    Doesnt work as well as i thought i would

    """
    for i in range(1, birdPd.shape[0]-sen*2):
        avgBefore = np.mean(birdPd.loc[i-sen:i, "Count"])
        current = birdPd.loc[i, "Count"]
        avgAfter = np.mean(birdPd.loc[i+1:i+sen+1, "Count"])
        if current < avgBefore and current < avgAfter:
            birdPd.loc[i, "Count"] = int((avgBefore+avgAfter)/2)
    return birdPd

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
    for i in range(0, birdPd.shape[0]-1):
        if birdPd.loc[i+1,"DateTime"].minute - birdPd.loc[i,"DateTime"].minute <= 2 :
            newBird.append([birdPd.loc[i,"DateTime"],birdPd.loc[i,"Count"]])
        elif birdPd.loc[i+1,"DateTime"].minute - birdPd.loc[i,"DateTime"].minute > 2 :
            gapMin = (birdPd.loc[i,"DateTime"].minute + birdPd.loc[i+1,"DateTime"].minute) /2
            newTime = datetime(year = birdPd.loc[i,"DateTime"].year, 
                                        month = birdPd.loc[i,"DateTime"].month, 
                                        day = birdPd.loc[i,"DateTime"].day, 
                                        hour = birdPd.loc[i,"DateTime"].hour,
                                        minute = int(gapMin))
            temp = [newTime, birdPd.loc[i,"Count"]]
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
    datePd = pd.DataFrame(dateList, columns=['year', 
                                             'month', 
                                             'day', 
                                             'hour', 
                                             'minute',
                                             'DateTime'])
    
    birdExtend = pd.merge(datePd, birdPd, on='DateTime') 
    #birdPd.set_index('DateTime', drop=True, inplace=True)
    birdMinutes = birdExtend.groupby(['year',
                                      'month', 
                                      'day', 
                                      'hour', 
                                      'minute'], 
                                     as_index=False).agg({'Count':'mean',
                                                      'DateTime':'mean'})
    return(birdMinutes)

def limitMontion(birdPd):
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

##debug
print("Shape unprocessed", birdPd.shape[0])
birdPd = dropWeird(birdPd)
print("Shape remove weird", birdPd.shape[0])
birdPd = fixMissingLine(birdPd)
print("Shape fixed missing date1", birdPd.shape[0])
birdPd = datePerMinute(birdPd)
print("Shape datePerMinute", birdPd.shape[0]) # why two index less 
birdPd = limitMontion(birdPd)
print("Shape limit Montion", birdPd.shape[0])
ax1 = birdPd.loc[1:238748,'Count'].plot()

#plotTEST
#birdPd.set_index('DateTime', drop=True, inplace=True)
#birdPd.loc['2015-01-25 13:10']
#birdPd.loc['2016-01-16 16:14']
#ax2 = birdPd.loc['2015-01-25 13:10':'2015-02-16 16:14'].plot()
