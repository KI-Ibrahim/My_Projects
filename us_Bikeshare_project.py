import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'newyorkcity': 'new_york_city.csv','newyork': 'new_york_city.csv','washington': 'washington.csv' }# previously there was space between newyorkcity
month_choices = ['january','february','march','april','may','june']
day_choices={1:'Sunday',2:'Monday',3:'Tuesday',4:'Wednesday',5:'Thursday',6:'Friday',7:'Saturday'}
    
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=input('please enter the city name. Please enter either Chicago, New york city or Washington: \n').casefold().replace(" ","")
    while city!="chicago" and city!="newyorkcity" and city!="newyork"  and city!="washington":
        city=input('The city you enter is not available for analysis.Please enter either Chicago, New york city or Washington.\n').casefold().replace(" ","")

    # get user input for month (all, january, february, ... , june) & for day of week (all, monday, tuesday, ... sunday)
    time_filter=input('Would you like to filter the data by month,day,both of them? please Type "none" for no time filter.\n').casefold().replace(" ","")
    while(time_filter!="month" and time_filter!="day" and time_filter!="both"and time_filter!="none"):
        time_filter=input('Please enter a valid response. The filteration is either by date, month or both of them? please Type "none" for no time filter.\n').casefold().replace(" ","")
    if time_filter=="none":
        month="all"
        day="all"
    elif time_filter=="both":
        month=input('Which month you like to analyze? January, February, March, April, May, June?.\n').casefold().replace(" ","")
        month_exist=month_choices.count(month)
        while month_exist<1:
            month=input("Please make sure to spell the month's name correctly. Please note that the system only provide data for the first 6 months of the year: January, February, March, April, May, June.\n").casefold().replace(" ","")
            month_exist=month_choices.count(month)
        day=input(""""Which day you like to analyze? Please enter the day as an integer where (1=sunday, 2=monday, 3=tuesday, etc)\n""")
        while not day.isnumeric():
            day=input(""""Please make sure to enter the day correctly. Please enter the day again where (1=sunday, 2=monday, 3=tuesday, etc)\n""")
    elif time_filter=="month":
        day="all"
        month=input('Which month you like to analyze? January, February, March, April, March, April, May, June?.\n').casefold().replace(" ","")
        month_exist=month_choices.count(month)
        while month_exist<1:
            month=input("Please make sure to spell the month's name correctly. Please note that the system only provide data for the first 6 months of the year: January, February, March, April, May, June.\n").casefold().replace(" ","")
            month_exist=month_choices.count(month)
    elif time_filter=="day":
        month="all"
        day=input('Which day you like to analyze? Please enter the day as an integer where (1=sunday, 2=monday, 3=tuesday, etc)\n')
        while not day.isnumeric():
            day=input(""""Please make sure to enter the day correctly. Please enter the day again where (1=sunday, 2=monday, 3=tuesday, etc)\n""")
            
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
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    # extract month and day of week from Start Time to create new columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month to create the new dataframe
    if month!="all":
        month=month_choices.index(month)+1
        df = df[df['month'] == month]
        
    # filter by day of week to create the new dataframe
    if day!="all":
        df = df[df['day_of_week'] == day_choices[int(day)]]
        
    if df.empty:
        print(" The time filteration you entered resulted in an empty dataframe. Please change the time filteration's input.\n")
        get_filters()

    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month & the most common day of week
    if (month=="all" and day=="all"):
        common_month=month_choices[df['month'].value_counts().idxmax()-1]
        common_day_of_week = df['day_of_week'].value_counts().idxmax()
        print ("The most common month is: {}, and the most common day is: {}\n".format(common_month ,common_day_of_week))
    
    elif (month=="all" and day!="all"):
        common_month=month_choices[df['month'].value_counts().idxmax()-1]
        print ("The most common month is: {}\n".format(common_month))
        
    elif (month!="all" and day=="all"):
        common_day_of_week = df['day_of_week'].value_counts().idxmax()
        print ("most common day of the week is: {}\n".format(common_day_of_week))
        
    # display the most common start hour
    common_start_hour= df['Start Time'].dt.hour.value_counts().idxmax()
    print ("Most common hour of day is: {}\n".format(common_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station=df['Start Station'].value_counts().idxmax()
    print ("Most common start station is: {}\n".format(common_start_station))

    # display most commonly used end station
    common_end_station=df['End Station'].value_counts().idxmax()
    print ("Most common end station is: {}\n".format(common_end_station))

    # display most frequent combination of start station and end station trip
    common_combination_station=df.groupby(['Start Station','End Station']).size().idxmax()
    print ("Most common trip from start to end is: {}\n".format(common_combination_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=(pd.to_datetime(df['End Time'])-df['Start Time']).sum()
    print ("Total travel time is: {}\n".format(total_travel_time))


    # display mean travel time
    mean_travel_time=(pd.to_datetime(df['End Time'])-df['Start Time']).mean()
    print ("Average travel time is: {}\n".format(mean_travel_time))

    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_categories=df['User Type'].value_counts()
    print ("Counts of the different user types Subscriber, Customer and Dependant are:\n{}\n".format(user_categories))
    #print ("Counts of each user type are Male: {}, Female: {}".format(gender_categories_male, gender_categories_female))

    # Display counts of gender
    if (city!="washington"): 
        gender_categories=df['Gender'].value_counts()
        print ("Counts of each gender are Male and Female:\n{}\n".format(gender_categories))
        
    # Display earliest, most recent, and most common year of birth
        print ("Earliest, most recent, most common year of birth are {}, {}, and {} respectively".format(df['Birth Year'].nsmallest(1).values[0],df['Birth Year'].nlargest(1).values[0], df['Birth Year'].value_counts().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def print_raw_data(df):
    """printing five rows of the raw data for the user. The code asks if the user would like to look at the next five rows 
from the raw data until the user mention that he doesn't want to see more"""
    i=0
    raw_data_print_flag=input("would you like to see the first five rows of the raw data? (yes, no).\n").casefold().replace(" ","")
    while raw_data_print_flag!="yes" and raw_data_print_flag!="no":
        raw_data_print_flag=input("Please enter a valid response. Would you like to see the first five rows of the raw data? (yes, no).\n").casefold().replace(" ","")
        
    while raw_data_print_flag=="yes":
        print ("\n")
        print (df[:][i:i+5],"\n")
        raw_data_print_flag=input("would you like to see the next five rows of the raw data? (yes, no).\n").casefold().replace(" ","")
        while raw_data_print_flag!="yes" and raw_data_print_flag!="no":
            raw_data_print_flag=input("Please enter a valid response. Would you like to see the next five rows of the raw data? (yes, no).\n").casefold().replace(" ","")
        i+=5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        print_raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n').casefold().replace(" ","")
        while restart!="yes" and restart!="no":
            restart=input("Please enter a valid response. Would you like to restart? Enter yes or no. ?\n").casefold().replace(" ","")
            
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()