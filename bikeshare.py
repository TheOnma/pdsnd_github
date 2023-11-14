import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

# create a function to ask users to input choices


def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    city = ''
    while True:
        city = input(
            'Would you like to see data for Chicago, New York City, or Washington? ').lower()
        if city in CITY_DATA:
            break
        else:
            print(
                'Invalid input. Please choose from Chicago, New York City, or Washington.')

    while True:
        month = input(
            'Which month? January, February, March, April, May, June, or all? ').lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print('Invalid input. Please choose a valid month or all.')

    while True:
        day = input(
            'Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all? ').lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print('Invalid input. Please choose a valid day or all.')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    try:
        df = pd.read_csv(CITY_DATA[city.lower()])
    except FileNotFoundError:
        print("The data file for the selected city was not found.")
        return None

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['Hour'] = df['Start Time'].dt.hour
    df['Month'] = df['Start Time'].dt.month
    df['Day of week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months_of_year = ['january', 'february',
                          'march', 'april', 'may', 'june']
        index_of_month = months_of_year.index(month) + 1
        df = df[df['Month'] == index_of_month]

    if day != 'all':
        df = df[df['Day of week'] == day.title()]

    return df


def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print('Most common month: ', df['Month'].value_counts().index[0])
    print('Most common day of week: ',
          df['Day of week'].value_counts().index[0])
    print('Most common start hour: ', df['Hour'].value_counts().index[0])

    print("\nThis took {} seconds.".format(round(time.time() - start_time, 1)))
    print('-'*40)


def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('Most common start station: ',
          df['Start Station'].value_counts().index[0])
    print('Most common end station: ',
          df['End Station'].value_counts().index[0])
    print(pd.DataFrame(df.groupby(['Start Station', 'End Station']).size(
    ).sort_values(ascending=False)).iloc[0])

    print("\nThis took {} seconds.".format(round(time.time() - start_time, 1)))
    print('-'*40)


def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()

    print('Total travel time: {} seconds'.format(round(total_travel_time, 1)))
    print('Mean travel time: {} seconds'.format(round(mean_travel_time, 1)))

    print("\nThis took {} seconds.".format(round(time.time() - start_time, 1)))
    print('-'*40)


def user_stats(df, city):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('Counts of user types: ', df['User Type'].value_counts())

    if city.lower() in ['chicago', 'new york city']:
        print('Counts of gender: ', df['Gender'].value_counts())
        print('Most earliest year of birth: ',
              int(df['Birth Year'].min()))
        print('Most recent year of birth: ',
              int(df['Birth Year'].max()))
        print('Most common year of birth: ',
              int(df['Birth Year'].mode()[0]))

    print("\nThis took {} seconds.".format(round(time.time() - start_time, 1)))
    print('-'*40)


def display_raw_data(df):
    i = 0
    raw = input("Would you like to see the raw data? Enter yes or no. ").lower()
    pd.set_option('display.max_columns', 200)

    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df[i:i+5])
            raw = input(
                "Would you like to see 5 more rows of the data? Enter yes or no. ").lower()
            i += 5
        else:
            raw = input(
                "\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()


def main():
    while True:
        city, month, day = get_filters()
        if city and load_data(city, month, day) is not None:
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)

            display_raw_data(df)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break


if __name__ == "__main__":
    main()
