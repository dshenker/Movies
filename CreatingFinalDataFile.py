#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 18:31:07 2020

@author: dshenker
"""
import pandas as pd
import numpy as np
import os
import datetime
#from datetime import date

def convert_to_datetime(date):
    format_str = '%d/%m/%Y'
    new_date = datetime.datetime.strptime(dates, format_str)
    return new_date

def addRollingFullnessAverage(curr_block):
    show_dates = curr_block['Show_Datetime'].unique()
    counter = 0
    curr_avg = 0
    #curr_block['Previous_Fullness'] = np.nan
    for date in show_dates:
        
        if counter != 0:
            curr_block.loc[curr_block['Show_Datetime'] == date,'Previous_Fullness'] = curr_avg
            counter = counter + 1
            day_fullness_avg = curr_block[curr_block['Show_Datetime'] == date]['Actual_Fullness'].mean()
            new_avg = (curr_avg * (counter - 1) + day_fullness_avg) / counter
            curr_avg = new_avg
            
        else:
            curr_block.loc[curr_block['Show_Datetime'] == date,'Previous_Fullness'] = 0
            counter = counter + 1
            day_fullness_avg = curr_block[curr_block['Show_Datetime'] == date]['Actual_Fullness'].mean()
            new_avg = (curr_avg * (counter - 1) + day_fullness_avg) / counter
            curr_avg = new_avg
    
    
    return curr_block


if __name__ == "__main__":
    os.chdir("/Users/dshenker/Desktop/Movie_Project/March_18_output")
    orig = pd.read_csv("/Users/dshenker/Desktop/Movie_Project/March_18_output/features_with_imdb_all.csv");
    dates = orig.loc[:, 'Show Date']
    orig = orig.loc[orig['Time Difference'] <= 90,:]
    
    #Set up column to specify if showing was on a weekend
    orig['Show_Datetime'] = pd.to_datetime(dates)
    orig['Week_Day'] = orig['Show_Datetime'].dt.dayofweek
    conditions = [(orig['Week_Day'] == 5) | (orig['Week_Day'] == 6) | (orig['Week_Day'] == 7)]
    night_conditions = [(orig['time'] >= 1140)]
    orig['Weekend'] = np.select(conditions, [1], default = 0)
    orig['Night'] = np.select(night_conditions, [1], default = 0)
    orig = orig.sort_values(['Title', 'Show_Datetime'], ascending = [True, True])
    movie_titles = orig['Title'].unique()
    orig['Previous_Fullness'] = np.nan
    for title in movie_titles:
        curr_block = orig[orig['Title'] == title]
        orig.loc[orig['Title'] == title,:] = addRollingFullnessAverage(curr_block)
    
    orig.to_csv('July_15_90MinCutoff_Final_WithID.csv', index = False)
    
    
    #Set up column to control rolling average of fullness for that movie