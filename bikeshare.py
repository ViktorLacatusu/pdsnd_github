# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 13:03:14 2021

@author: Q359448
"""

import time
import pandas as pd
import numpy as np
import random as rd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """ Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
   
    # get user input for city (chicago, new york city, washington)
    cities = {'chicago', 'new york city', 'washington'}
    city = 'empty'
    while city not in cities:
        print('Which data would you like to look at?')
        city = input('Please enter chicago, new york city or washington:\n').lower()
        
    # get user input for month as int value or deactivate month filter (all, january, february, ... , june)
    month = input('Would you like to filter the data by month? Enter "yes" or "no":\n').lower()
    # if user input = "yes" then get month as int
    if month == 'yes':
        print('Which month are you interested in?')
        month = 0
        # get month as int value while user input != month nr from 1 to 6 (e.g. 1 = January..)
        while month not in range(1,7):
            month = input("Please enter a number from 1 to 6 (e.g. 1 = January .. 6 = June):\n")
            month = int(month)
    # if user input != "yes" set month = 'all' to deactivate month filter
    else: month = 'all'

    # get user input for day of week as int value or deactivate day filter (all, monday, tuesday, ... sunday)
    day = input('Would you like to filter the data by day? Enter "yes" or "no":\n').lower()
    # if user input = "yes" then get weekday as int
    if day == 'yes':
        day = 0
        # get weekday as int value while user input != day nr from 1 to 7 (e.g. 1 = Monday..)
        while day not in range(1,8):
            day = input("Please enter a number from 1 to 7 (e.g. 1 = Monday .. 7 = Sunday):\n")
            day = int(day)
    # if user input != "yes" set day = 'all' to deactivate weekday filter
    else: day = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
   
    # load data file into a dataframe (df)
    df = pd.read_csv(CITY_DATA[city])
    
    # display general data information (selected data set, total nr of records, first entry, last entry)
    print('Selected data set: ', city.title())
    print('Total number of records without time filter: ', df['Start Time'].count())
    print('First entry: ', df['Start Time'].min())
    print('Last entry: ', df['Start Time'].max())

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, weekday and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month to create the new dataframe if month filter is active (month != "all")
    if month != 'all':
        df = df[df['month'] == month]

    # filter by day of week to create the new dataframe if day filter is active (day != "all")
    if day != 'all':
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        df = df[df['weekday'] == weekdays[day-1]]

    print('-'*40)
    return df
        
def time_stats(df):
    """ Displays statistics on the most frequent times of travel.
    
    Args:
        (df) dataframe - Pandas DataFrame containing relevant bikeshare records
    
    Returns:
        Most Common Month - Month that occurs most often in the evaluated user data
        Most Common Weekday - Day that occurs most often in the evaluated user dat
        Most Common Hour - Start Time that occurs most often in the evaluated user dat
   
    Note: 
        No variables will be returned - function only displays certain calculated stats
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert "Start Time" to datatype datetime    
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    most_common_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('Most Common Month:', (months[most_common_month-1]))
    
    # display the most common day of week
    most_common_weekday = df['weekday'].mode()[0]
    print('Most Common Weekday:', most_common_weekday)

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('Most Common Hour: {} o\'clock'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """ Displays statistics on the most popular stations and trip.
      
    Args:
        (df) dataframe - Pandas DataFrame containing relevant bikeshare records
    
    Returns:
        Most Common Start Station - Start Station that occurs most often in the evaluated user data
        Most Common End Station - End Station that occurs most often in the evaluated user dat
        Most Common Route - Route (Start to End Station) that occurs most often in the evaluated user dat
    
    Note: 
        No variables will be returned - function only displays certain calculated stats
    """
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most Used Start Station:', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most Used End Station:', most_common_end_station)

    # display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + ' -> ' + df['End Station']
    most_common_route = df['Route'].mode()[0]
    print('Most Common Route:', most_common_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """ Displays statistics on the total and average trip duration.
        
    Args:
        (df) dataframe - Pandas DataFrame containing relevant bikeshare records
    
    Returns:
        Total Duration in sec -  Calculates the sum of all travel times within the data set
        Average Duration in sec - Calculates the average of all travel times within the data set
           
    Note: 
        No variables will be returned - function only displays certain calculated stats
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Duration in sec: {}'.format(df['Trip Duration'].sum()))
    print('Trip Count: {}'.format(df['Trip Duration'].count()))

    # display mean travel time
    print('Average Duration in sec: {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """ Displays statistics on bikeshare users.
            
    Args:
        (df) dataframe - Pandas DataFrame containing relevant bikeshare records
    
    Returns:
        Gender Types -  Calculates the sum of all travel times within the data set
        Earliest year of birth - Calculates the average of all travel times within the data set
        Most recent year of birth - The most recent year of birth found in the evaluated user data
        Most common year of birth - Year of birth that occurs most often in the evaluated user data
        
    Notes: 
        No variables will be returned - function only displays certain calculated stats
        Check if gender and birth date in included in the data set first, before calculating stats    
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    print(df.groupby(['User Type'])['User Type'].count())

    # check if gender is included and display counts of gender male/female incl. unknown records
    try:
        print(df.groupby(['Gender'])['Gender'].count())
        print('Gender is for {} unknown!'.format(df['Gender'].isnull().sum()))
    # display if gender is not included
    except KeyError:
        print('The category "Gender" is not included in the dataset!')

    # check if birth date is included and display earliest, most recent, and most common year of birth
    try:
        print('Earliest year of birth: {}'.format(df['Birth Year'].min()))
        print('Most recent year of birth: {}'.format(df['Birth Year'].max()))
        print('Most common year of birth: {}'.format(df['Birth Year'].mode()[0]))
    # display if birth date is not included
    except KeyError:
        print('The category "Birth Year" is not included in the dataset!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def random_record(df):
    """ Displays random trip records until the user doesn't want to see any more dates
                
    Args:
        (df) dataframe - Pandas DataFrame containing relevant bikeshare records
    
    Returns:
        A random data record from the selected data set by using sample() 
        
    Notes: 
        No variables will be returned - Function only displays random data records
    """
      
    # ask user if a random trip record should be displayed and get user response
    random_stats = input('Would you like to look at some random costumer data? Enter "yes" or "no":\n').lower()
    
    # check user response and display random data records aslong resppnse == "yes"
    while random_stats == 'yes':
        # get random trip record from the data set and display stats 
        print('-'*40)
        df_random = df.sample(1)
        for item in df_random:
            print(df_random[item])
        print('-'*40)   
        
        # ask user for more random records and get user response
        random_stats = input('Would you like to see more random costumer data? Enter "yes" or "no":\n').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        random_record(df) 

        restart = input('Would you like to restart? Enter "yes" or "no":\n').lower()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
