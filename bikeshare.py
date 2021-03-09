import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
filter = ''

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    while 1:
        city = str(input('Would you like to see data for Chicago, New York or Washinton? \n')).lower()
        if city in cities:
           break
        else:
           print("Incorrect value")

    #get user input for month (all, january, february, ... , june)
    months = set(['january', 'february', 'march', 'april', 'may', 'june', 'all'])
    while 1:
        month = str(input('Which month: january, february, march, april, may, june, all \n')).lower()
        if month in months:
            break
        else:
            print("Incorrect value")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days_of_week =  set(['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all' ])
    while 1:
        day = str(input('Which day: monday, tuesday, wednesday, thrusday, friday, saturday, sunday, all: \n')).lower()
        if day in days_of_week:
           break
        else:
            print("Incorrect value")

    global filter
    if (month != 'all' and day != 'all'):
        filter = 'both'
    elif (month == 'all' and day != 'all'):
        filter = 'day'
    elif (month != 'all' and day == 'all'):
        filter = 'month'
    else:
        filter = 'none'
    #print('The filter is', filter)

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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    #df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def see_raw_data(df, city):
    """
    Display raw data of a dp.

    Args:
        (str) city - name of the city to analyze
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        none
    """
    if (city != 'all'):
        #index = 5
        total_rows = len(df) - 5
        start = 0
        end = 5
        while (1):
            if start == 0:
                restart = input('\nWould you like see the the first 5 rows of {}.csv ? Enter yes or no.\n'.format(city))
                if restart.lower() != 'yes':
                    break
                else:
                    #print(df.head(index))
                    print(df[start:end])
                    #index +=5
                    start += 5
                    end += 5

            else:
                restart = input('\nWould you like see the next 5 lines ? Enter yes or no.\n')
                if restart.lower() != 'yes':
                    break
                elif (total_rows - end) >= 0:
                    #print(df.head(index))
                    print(df[start:end])
                    start += 5
                    end += 5
                    #index += 5
                else:
                    break

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # [Mario Sanz:] if we are filtering by it does no make sense
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Most popular month is',months[popular_month-1])


    # display the most common day of week
    # [Mario Sanz:] if we are filtering by it does no make sense
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most popular day of week is',popular_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    count = df['hour'].value_counts().max()
    #global filter
    print('Most popular start hour: {}, Count {}, Filter {}'.format(popular_hour, count, filter))
    #print('Count', df['hour'].value_counts().max())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    count = df['Start Station'].value_counts().max()
    print('Most Commonly used start station: {}, Count {}'.format(start_station, count))
    print()

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    count = df['End Station'].value_counts().max()
    print('Most Commonly used end station: {}, Count {}'.format(end_station, count))
    print()

    # display most frequent combination of start station and end station trip
    print('Star_End_Station_Method_1')
    df['Start_End_Station'] = 'Start Station: ' + df['Start Station'] + ' / End Station ' + df['End Station']
    star_end_station = df['Start_End_Station'].mode()[0]
    count = df['Start_End_Station'].value_counts().max()
    print('Most Commonly used start_end station: {}, Count {}'.format(star_end_station, count))
    print()

    print('Star_End_Station_Method_2')
    #frequent_stations = df.groupby(['Start Station','End Station']).size().nlargest(1)
    #print('Most frequent start and end station: ', df.groupby(['Start Station','End Station']).size().nlargest(1))
    print('Most frequent start and end station:')
    print(df.groupby(['Start Station','End Station']).size().nlargest(1))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trv_time_raw = int(df['Trip Duration'].sum())
    total_trv_time = datetime.timedelta(seconds=total_trv_time_raw)
    print('Total Travel Time (HH:MM:SS): ', total_trv_time)
    print()

    #display mean travel time
    mean_trv_time_raw = int(df['Trip Duration'].mean())
    mean_trv_time = datetime.timedelta(seconds=mean_trv_time_raw)
    print('Mean Travel Time (HH:MM:SS): ', mean_trv_time)
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types: ', df['User Type'].value_counts())
    print()


    labels = list(df)
    #Display counts of gender
    if 'Gender' in labels:
        print('Counts of user gender: ', df['Gender'].value_counts())
        print()

    #Display earliest, most recent, and most common year of birth
    if 'Birth Year' in labels:
        most_recent = max(df['Birth Year'])
        earliest = min(df['Birth Year'])
        most_common = df['Birth Year'].mode()[0]
        print('Earliest Year: {} / Most Recent Year: {} / Most Common Year: {}'.format(earliest, most_recent, most_common))
        print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        see_raw_data(df, city)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        #print(df.head())

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
