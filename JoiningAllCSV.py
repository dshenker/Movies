o#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 21:04:55 2020

@author: dshenker
"""
import pandas as pd
import numpy as np
import os
from datetime import date


os.chdir("/Users/dshenker/Desktop/Movie-project-data")


movies_full = pd.DataFrame()
col_choice = ["percent full", "price", "time", "Time Taken"]       
    
for WorkingFile in os.listdir('/Users/dshenker/Desktop/Movie-project-data'): 
    print(WorkingFile)
    if WorkingFile == ".DS_Store":
        continue
    
    date_portion = WorkingFile[22:]
    space = date_portion.find(' ')
    month = date_portion[:space]
    if month == "February":
        month_num = 2
    else:
        month_num = 3
    comma = date_portion.find(',')
    day_num = int(date_portion[space + 1:comma])
    year = 2020
    show_date = date(year, month_num, day_num)
    print(show_date)
    df_movies = pd.read_csv(WorkingFile, index_col = "title")
    df_movies = df_movies.drop("Unnamed: 0", axis = 1)
    df_movies = df_movies.dropna()
    #print(df_movies.count)
    if df_movies.shape[0] == 0:
        continue

    #print(df_movies)
    num_rows = df_movies.shape[0]
    #print("number of rows in this frame")
    #print(num_rows)
    df_movies["price"] = df_movies["price"].replace("$", "")
    
    df_movies_sub = df_movies[col_choice]
    
    
    #print(df_movies_sub)
    df_movies_sub.iloc[:, 0] = df_movies_sub.iloc[:, 0].astype(str).str.replace(r"Gross USA:", '')
    df_movies_sub.iloc[:, 0] = df_movies_sub.iloc[:, 0].str.replace(r"$", '')
    df_movies_sub.iloc[:, 0] = df_movies_sub.iloc[:, 0].str.replace(r" ", '')
    df_movies_sub.iloc[:, 0] = df_movies_sub.iloc[:, 0].astype(str).str.replace(r",", '').astype(float)
    df_movies_sub.iloc[:, 1] = df_movies_sub.iloc[:, 1].str.replace(r"$", '').astype(float)
    time_entries = np.array(df_movies["time"])
    
    ending = np.array([x[-1:] for x in time_entries.astype(str)])
    morning_times = list(np.transpose(np.where(ending == 'a')))
    evening_times = list(np.transpose(np.where(ending == 'p')))
    
    for i,time in enumerate(df_movies_sub.iloc[:, 2]):
        hour_in_minutes = 0
        minute = 0
        colon_index = time.find(':')
        hour = (int)(time[0:colon_index])
        minute = (int)(time[colon_index + 1:colon_index + 3])
        if hour != 12:
            hour_in_minutes = hour * 60;
        if evening_times.count(i) > 0: 
            hour_in_minutes = hour_in_minutes + 720
        minute_total = hour_in_minutes + minute
        time = minute_total
        df_movies_sub.iloc[i,2] = time
    
    for i, time in enumerate(df_movies_sub.iloc[:, 3]):
        hour_in_minutes = 0
        minute = 0
        time = time[:-3]
        colon_index = time.find(':')
        hour = (int)(time[0:colon_index])
        minute = (int)(time[colon_index + 1:colon_index + 3])
        hour_in_minutes = hour * 60
        minute_total = hour_in_minutes + minute
        time = minute_total
        df_movies_sub.iloc[i, 3] = time
    
    df_movies_sub["Time Difference"] = df_movies_sub["time"] - df_movies_sub["Time Taken"]
    df_movies_sub["Show Date"] = show_date
    df_movies_sub["money missed"] = df_movies.iloc[:, 0]
    
    df_scaled = df_movies_sub.copy()
    average_pct = df_scaled["percent full"].mean()
    df_scaled["theater identifier"] = average_pct
       
   
    movies_full = pd.concat([movies_full, df_scaled])
    

    
#features = ["price", "time", "Time Taken", "Time Difference", "theater identifier"]         
output = ["percent full"]
X = movies_full.drop("percent full", axis = 1)

y = movies_full[output]
os.chdir("/Users/dshenker/Desktop/March_18_output")
X.to_csv("features_recent_all.csv")
y.to_csv("percents_recent_all.csv")

