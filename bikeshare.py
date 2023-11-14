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
        bikeshare_data = pd.read_csv(CITY_DATA[city.lower()])
    except FileNotFoundError:
        print("The data file for the selected city was not found.")
        return None

    bikeshare_data['Start Time'] = pd.to_datetime(bikeshare_data['Start Time'])
    bikeshare_data['End Time'] = pd.to_datetime(bikeshare_data['End Time'])

    bikeshare_data['Hour'] = bikeshare_data['Start Time'].dt.hour
    bikeshare_data['Month'] = bikeshare_data['Start Time'].dt.month
    bikeshare_data['Day of week'] = bikeshare_data['Start Time'].dt.weekday_name

    if month != 'all':
        months_of_year = ['january', 'february',
                          'march', 'april', 'may', 'june']
        index_of_month = months_of_year.index(month) + 1
        bikeshare_data = bikeshare_data[bikeshare_data['Month']
                                        == index_of_month]

    if day != 'all':
        bikeshare_data = bikeshare_data[bikeshare_data['Day of week'] == day.title(
        )]

    return bikeshare_data


def time_stats(bikeshare_data):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print('Most common month: ',
          bikeshare_data['Month'].value_counts().index[0])
    print('Most common day of week: ',
          bikeshare_data['Day of week'].value_counts().index[0])
    print('Most common start hour: ',
          bikeshare_data['Hour'].value_counts().index[0])

    print("\nThis took {} seconds.".format(round(time.time() - start_time, 1)))
    print('-'*40)


def station_stats(bikeshare_data):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('Most common start station: ',
          bikeshare_data['Start Station'].value_counts().index[0])
    print('Most common end station: ',
          bikeshare_data['End Station'].value_counts().index[0])
    print(pd.DataFrame(bikeshare_data.groupby(['Start Station', 'End Station']).size(
    ).sort_values(ascending=False)).iloc[0])

    print("\nThis took {} seconds.".format(round(time.time() - start_time, 1)))
    print('-'*40)


def trip_duration_stats(bikeshare_data):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = bikeshare_data['Trip Duration'].sum()
    mean_travel_time = bikeshare_data['Trip Duration'].mean()

    print('Total travel time: {} seconds'.format(round(total_travel_time, 1)))
    print('Mean travel time: {} seconds'.format(round(mean_travel_time, 1)))

    print("\nThis took {} seconds.".format(round(time.time() - start_time, 1)))
    print('-'*40)


def user_stats(bikeshare_data, city):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('Counts of user types: ', bikeshare_data['User Type'].value_counts())

    if city.lower() in ['chicago', 'new york city']:
        print('Counts of gender: ', bikeshare_data['Gender'].value_counts())
        print('Most earliest year of birth: ',
              int(bikeshare_data['Birth Year'].min()))
        print('Most recent year of birth: ',
              int(bikeshare_data['Birth Year'].max()))
        print('Most common year of birth: ',
              int(bikeshare_data['Birth Year'].mode()[0]))

    print("\nThis took {} seconds.".format(round(time.time() - start_time, 1)))
    print('-'*40)


def display_raw_data(bikeshare_data):
    i = 0
    view_raw_data = input(
        "Would you like to see the raw data? Enter yes or no. ").lower()
    pd.set_option('display.max_columns', 200)

    while True:
        if view_raw_data == 'no':
            break
        elif view_raw_data == 'yes':
            print(bikeshare_data[i:i+5])
            view_raw_data = input(
                "Would you like to see 5 more rows of the data? Enter yes or no. ").lower()
            i += 5
        else:
            view_raw_data = input(
                "\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()


def main():
    while True:
        city, month, day = get_filters()
        if city and load_data(city, month, day) is not None:
            bikeshare_data = load_data(city, month, day)

            time_stats(bikeshare_data)
            station_stats(bikeshare_data)
            trip_duration_stats(bikeshare_data)
            user_stats(bikeshare_data, city)

            display_raw_data(bikeshare_data)

            restart_prompt = input(
                '\nWould you like to restart? Enter yes or no.\n')
            if restart_prompt.lower() != 'yes':
                break


if __name__ == "__main__":
    main()
