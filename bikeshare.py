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
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = 'empty'
    counter = 2
    while city not in ('c','n','w'):
        print('Which data would you like to look at?')
        city = input('Type "c" for Chicago, "n" for New York City or "w" for Washington DC:\n')
        
        if city not in ('c','n','w'):
            print('Open attempts: {} - Only c/n/w in small letters are allowed!\n'.format(counter))
            counter -= 1
        
        if counter < 0:
            print('\n GAME OVER -> A random data set will be selected!\n')
            cities =["c","n","w"]
            city = rd.choice(cities)
            break;

    # match user input to city name
    if city == "c":
         city = "chicago"
    elif city == "n":
         city = "new york city"
    elif city == "w":
         city = "washington"

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Would you like to filter the data by month? Enter "yes" or "no":\n')
    if month == 'yes':
        print('Which month are you interested in?')
        month = 0
        while month not in range(1,7):
            month = input("Please enter a number from 1 to 6 (e.g. 1 = January .. 6 = June):\n")
            month = int(month)
    else: month = 'all'

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Would you like to filter the data by day? Enter "yes" or "no":\n')
    if day == 'yes':
        day = 0
        while day not in range(1,8):
            day = input("Please enter a number from 1 to 7 (e.g. 1 = Monday .. 7 = Sunday):\n")
            day = int(day)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # display general data information
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

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        df = df[df['weekday'] == weekdays[day-1]]

    print('-'*40)
    return df
        
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Convert "Start Time" to datatype datetime    
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('Most Common Month:', (months[most_common_month-1]))
    
    # TO DO: display the most common day of week
    most_common_weekday = df['weekday'].mode()[0]
    print('Most Common Weekday:', most_common_weekday)

    # TO DO: display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('Most Common Hour: {} o\'clock'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most Used Start Station:', most_common_start_station)

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most Used End Station:', most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
c    df['Route'] = df['Start Station'] + ' -> ' + df['End Station']
    most_common_route = df['Route'].mode()[0]
    print('Most Common Route:', most_common_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# OK
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total Duration in sec: {}'.format(df['Trip Duration'].sum()))
    print('Trip Count: {}'.format(df['Trip Duration'].count()))

    # TO DO: display mean travel time
    print('Average Duration in sec: {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df.groupby(['User Type'])['User Type'].count())

    # TO DO: Display counts of gender
    try:
        print(df.groupby(['Gender'])['Gender'].count())
        print('Gender is for {} unkown!'.format(df['Gender'].isnull().sum()))
    except KeyError:
        print('The category "Gender" is not included in the dataset!')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print('Earliest year of birth: {}'.format(df['Birth Year'].min()))
        print('Most recent year of birth: {}'.format(df['Birth Year'].max()))
        print('Most common year of birth: {}'.format(df['Birth Year'].mode()[0]))
    except KeyError:
        print('The category "Birth Year" is not included in the dataset!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# new small function added to the template
def random_record(df):
    """Displays a random trip record using the module random."""
      
    # ask user if a random trip record should be displayed 
    random_stats = input('Would you like to look at some random costumer data? Enter "yes" or "no":\n')
    
    # display random trip record 
    while random_stats == 'yes':
        print('-'*40)
        df_random = df.sample(1)
        for item in df_random:
            print(df_random[item])
        print('-'*40)   
        
        # ask user for more random records 
        random_stats = input('Would you like to see more random costumer data? Enter "yes" or "no":\n')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        # add new small function
        random_record(df) 

        restart = input('Would you like to restart? Enter "yes" or "no":\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
