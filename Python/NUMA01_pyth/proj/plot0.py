#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 18:38:24 2022

@author: supamafia
"""

import merge0 as pre

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

def datePerMinute(birdPd):
    """
    Reduce to data per minute first
    Add columns that reperesent year, monnth, week, day, hour, and minute.
    It is a requisite for the correctInterval function
    """
    dateList = []
    for i in tqdm(range(birdPd.shape[0])):
        temp = [birdPd.loc[i,'DateTime'].year, 
                birdPd.loc[i,'DateTime'].month,
                birdPd.loc[i, 'DateTime'].isocalendar().week,
                birdPd.loc[i,'DateTime'].day,
                birdPd.loc[i,'DateTime'].hour,
                birdPd.loc[i,'DateTime'].minute,
                birdPd.loc[i,'DateTime']]
        dateList.append(temp)
    datePd = pd.DataFrame(dateList, columns=['year', 
                                             'month',
                                             'week',
                                             'day', 
                                             'hour', 
                                             'minute',
                                             'DateTime'])
    birdExtend = pd.merge(datePd, birdPd, on='DateTime') 
    
    birdMinutes = birdExtend.groupby(['year',
                                      'month',
                                      'week',
                                      'day', 
                                      'hour', 
                                      'minute'], 
                                     as_index=False).agg({'Count':'mean',
                                                      'DateTime':'mean'})
                                                          
    return(birdExtend)

def diff(birdPd):
    birdDiff = []
    for i in range(birdPd.shape[0]-1):
        tempCount = birdPd.loc[i + 1, 'Count'] - birdPd.loc[i , 'Count']
        temp = [abs(tempCount), birdPd.loc[i , 'DateTime']]
        birdDiff.append(temp)
    birdDiffPd = pd.DataFrame(birdDiff, columns=['Count', 'DateTime'])
    return birdDiffPd

# Are there motions when it is darks
# sSandby = ast.Observer(latitude = 55.71688, longitude = 13.34663)

def isDayTime(birdPd, location= ast.Observer(latitude = 55.71688, longitude = 13.34663)):
    """
    Add a new column to dataframe called isDaytime
    default for location is:
        sSandby = ast.Observer(latitude = 55.71688, longitude = 13.34663)
    """
    isDayTime = []
    for i in tqdm(range(birdPd.shape[0])):
        t0 = datetime.timestamp(ast.sun(location, birdPd.loc[i,'DateTime']).get('sunrise'))
        t1 = datetime.timestamp(ast.sun(location, birdPd.loc[i,'DateTime']).get('sunset'))
        t = datetime.timestamp(birdPd.loc[i,'DateTime'])
        if t > t0 and t< t1:
            isDayTime.append(True)
        else:
            isDayTime.append(False)
    isDayTimePd = pd.DataFrame(isDayTime, columns=['isDayTime'])
    birdPd = birdPd.join(isDayTimePd)
    return (birdPd)

def drawNight(birdPd, start=0, end=500, prety0 = 'C1', prety='blue', a0=0.3):
    """
    Drawing function, returns a plot which nigh is shaded. 

    """
    lower = 0
    upper = 0
    dayStart = []
    plt.style.use('default')
    fig, ax1 = plt.subplots(1, 1)
    #ax1 = birdPd.loc[start:end,'Count'].plot()
    ax1.plot(birdPd.loc[start:end,'DateTime'], birdPd.loc[start:end,'Count'], color = prety0)
    for i in tqdm(range(start, end-1)):
        if birdPd.iloc[i].at["isDayTime"] == True and birdPd.iloc[i+1].at["isDayTime"] == False:
            lower = i
        if birdPd.iloc[i].at["isDayTime"] == False and birdPd.iloc[i+1].at["isDayTime"] == True:
            upper = i-1
            if lower != 0 and upper != 0:
                ax1.axvspan(birdPd.loc[lower,'DateTime'], birdPd.loc[upper,'DateTime'], color = prety, alpha = a0)
                lower = 0
                upper = 0
    ax1.xaxis.set_major_locator(mdates.DayLocator()) # plots marjor tick on dates
    ax1.xaxis.set_minor_locator(mdates.HourLocator()) # plots minor ticks on hour
    for label in ax1.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')
    
    ax1.grid(True, color='0.4', linestyle='--', linewidth=0.5)
    ax1.set_ylabel('Count')
    ax1.set_xlabel('Date')
    plt.show()
    return ax1

def strDayToInd(birdPd, strDate, dateDelta = 0, dateForm='%Y-%m-%d %H:%M'):
    """
    Function that take dataframe, and string Date and returns the Date's corresponding index in the dataframe

    """
    date = datetime.strptime(strDate, dateForm)
    if dateDelta != 0:
        date = date + timedelta(days = dateDelta)
        
    date = datetime.timestamp(date)
    for i in tqdm(range(birdPd.shape[0]-1)):
        t0 = datetime.timestamp(birdPd.loc[i,'DateTime'])
        t1 = datetime.timestamp(birdPd.loc[i+1,'DateTime'])
        if t0 == date:
            return i
        if t1 == date:
            return i
        if t0 > date and date < t1:
            return i

def correctInterval(birdPd, strInterval):
    """
    This function groups Count, as average, by hour, day, week, month or year

    prequisite to run the function is run datePerMinute(birdPd)

    """
    if strInterval == 1 :#"total per hour" 
        birdNew = birdPd.groupby(['year',
                                  'month',
                                  'week',
                                  'day', 
                                  'hour'], 
                                  as_index=False).agg({'Count':'mean',
                                                       'DateTime':'mean'})
    if strInterval == 2 :#"total per day"
        birdNew = birdPd.groupby(['year',
                                  'month',
                                  'week',
                                  'day'], 
                                  as_index=False).agg({'Count':'mean',
                                                       'DateTime':'mean'})
    if strInterval == 3 :#"total per week"
        birdNew = birdPd.groupby(['year',
                                  'month',
                                  'week'], 
                                  as_index=False).agg({'Count':'mean',
                                                       'DateTime':'mean'})
    if strInterval == 4 :#"total per month"
        birdNew = birdPd.groupby(['year',
                                  'month'], 
                                  as_index=False).agg({'Count':'mean',
                                                       'DateTime':'mean'})
    if strInterval == 5 :#"total per year"
        birdNew = birdPd.groupby(['year'], 
                                  as_index=False).agg({'Count':'mean',
                                                       'DateTime':'mean'})
    return birdNew

def normalPlot(birdPd, startDate, numDays, interval, dateForm='%Y-%m-%d %H:%M'):
    """
    Comply to the input requirement of TASK 4. It takes start date, number of days, and interval.
    And it plot the Count accordingly

    """
    if numDays > 14:
        print('Date axis could be too clustered. Try reduce the number of dates')
    birdPd = correctInterval(birdPd, interval)
    ind0 = strDayToInd(birdPd, startDate, 0, dateForm)
    ind1 = strDayToInd(birdPd, startDate, numDays, dateForm)
    plt.style.use('default')
    fig, ax1 = plt.subplots(1, 1)
    ax1.plot(birdPd.loc[ind0:ind1,'DateTime'], birdPd.loc[ind0:ind1,'Count'], color = 'C1')
    ax1.xaxis.set_major_locator(mdates.DayLocator()) # plots marjor tick on dates
    ax1.xaxis.set_minor_locator(mdates.HourLocator()) # plots minor ticks on hour
    for label in ax1.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')
    
    ax1.grid(True, color='0.4', linestyle='--', linewidth=0.5)
    ax1.set_ylabel('Count')
    ax1.set_xlabel('Date')
    plt.show()
    return ax1                                                     

def deBugPlot(birdPd):
    """
    Take data frame and plot all count values.

    """
    fig, ax1 = plt.subplots(1, 1)
    ax1.plot(birdPd.loc[:,'DateTime'], birdPd.loc[:, 'Count'])
    plt.show()
    return ax1

def bargraphs(birdPd): 
    # change over year
    fig0, ax0 = plt.subplots()
    """
    First, we cannot compare year on year since 2016 only has 1 month of data.
    But, it is also not fair to compare the last half of janurary of 2015
    to the fist half of january of 2016.
    """
    birdYear = correctInterval(birdDiff_m, 4)
    compareYear = birdYear.loc[birdYear.month == 1]
    ax0.bar(list(['2015-Jan' , '2016-Jan']), compareYear.loc[:,'Count'])
    ax0.set_xlabel('Year')
    ax0.set_ylabel('Average movement per minute')
    plt.show()

    # feeding period, breeding period
    fig1, ax1 = plt.subplots()
    """
    There is a lot of movement in the later half of the night, from about 1 to 7.
    It could be result of the start of twilight which shifts around during the year.
    There is less movement during the day. From about 8 to 11. 
    But the movement increases again during 12 to 17 during drawn. 
    There is minimal movement during the first half of night around clock 20.
    Feeding period in a day is between from 24 to 7, and from 12 to 16.
    """
    birdHourDiff = birdDiff_m.groupby(['hour'], 
                              as_index=False).agg({'Count':'mean',
                                                   'hour':'mean'})
    hourList = list([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
    ax1.bar(hourList, birdHourDiff.loc[: ,'Count'])
    ax1.set_xlabel('Hour')
    ax1.set_ylabel('Average movement per minute')
    plt.show()

    fig2, ax2 = plt.subplots()
    """
    There is a graduate increase of movement from Janurary to April.
    There is a lot of activity in May. 
    The movement is still high during June and July.
    And the movement is minial during the later half of the year, from August to December.
    Thus, the breeding period is in spring and early summer.
    """
    birdMonthDiff = birdDiff_m.groupby(['month'], 
                              as_index=False).agg({'Count':'mean',
                                                   'month':'mean'})
    monthList = list([1,2,3,4,5,6,7,8,9,10,11,12])
    plt.bar(monthList, birdMonthDiff.loc[: ,'Count']) 
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Average movement per minute')
    plt.show()

# create dataframe to plot
birdPd = pre.runPre() # run pre processing
birdDiff = diff(birdPd) # create diff by day dataframe
deBugPlot(birdPd)
deBugPlot(birdDiff)
birdPd_m = datePerMinute(birdPd) # aggregate to minutes
birdDiff_m = datePerMinute(birdDiff) # aggregate to minutes
birdPd = isDayTime(birdPd) # new column for day night visual

# plots
# plot day night cycle
drawNight(birdPd, strDayToInd(birdPd, '2015-08-12 0:00'), strDayToInd(birdPd, '2015-08-13 23:59'))
# plot by inputs
normalPlot(birdPd_m, '2015-08-5 9:31', 14, 1)
normalPlot(birdPd_m, '2015-04-5 9:31', 14, 1)
bargraphs(birdPd)

