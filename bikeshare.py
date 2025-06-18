import time
import calendar
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data!\nYou\'ll be selecting a city, month and day to filter your data.')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWhich city would you like to explore? chicago, new york city or washington?\n").strip().lower()
        if city in CITY_DATA:
            print('-' * 70)
            break
        else: 
            print('Invalid input, Please choose one of the following cities: Chicago, New York City or Washington')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWhich month would you like to filter the data by, type 'all' to include every month.\n").strip().title()
        if month == 'All' or month in list(calendar.month_name[1:7]):
            print('-' * 70)
            break
        else: 
            print('Invalid input, Please choose a month from January to June:')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWhich day of the week would you like to filter the data by, type 'all' to include all days.\n").strip().title()
        if day == 'All' or day in list(calendar.day_name):
            break
        else: 
            print('Invalid input, Please choose a day from Monday to Sunday:')

    print('-'*70)
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'All':
        df = df[df['Month'] == month]

    if day != 'All':
        df = df[df['Day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print(f"The most common month of travel is: {df['Month'].mode()[0]}")

    # display the most common day of week
    print(f"The most common day of travel is: {df['Day'].mode()[0]}")

    # display the most common start hour
    print(f"The most common hour of travel is: {df['hour'].mode()[0]}")

    print(f"\nThis took {time.time() - start_time:.5f} seconds.")
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"Most commonly used start station: {df['Start Station'].mode()[0]}")

    # display most commonly used end station
    print(f"Most commonly used end station: {df['End Station'].mode()[0]}")

    # display most frequent combination of start station and end station trip
    trip = df[['Start Station', 'End Station']].value_counts().idxmax()
    print("Most frequent combination of start station and end station trip:",
    f"{trip[0]} ---> {trip[1]}")

    print(f"\nThis took {time.time() - start_time:.5f} seconds.")
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['End Time'] - df['Start Time']
    total_time = travel_time.sum()
    print(f"Total travel time = {format_timedelta(total_time)}")

    # display mean travel time
    mean_time = travel_time.mean()
    print(f"Mean travel time = {format_timedelta(mean_time)}")

    print(f"\nThis took {time.time() - start_time:.5f} seconds.")
    print('-'*40)

def format_timedelta(td):
    """Formats timedelta into days/hours/minutes/second."""
    
    return (f"{td.days} days, {td.seconds // 3600} hours, "
            f"{td.seconds % 3600 // 60} minutes, {td.seconds % 60} seconds")

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f"Counts of users' types:\n{df['User Type'].value_counts()}\n")

    # Display counts of gender
    if 'Gender' in df.columns:
        print(f"Counts of users' genders:\n{df['Gender'].value_counts()}\n")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print(f"Earliest year of birth: {df['Birth Year'].min()}\n"
        f"Most recent year of birth: {df['Birth Year'].max()}\n"
        f"Most common year of birth: {df['Birth Year'].mode()[0]}")

    print(f"\nThis took {time.time() - start_time:.5f} seconds.")
    print('-'*40)

def display_data(df):
    index = 0
    while True:
        display = input("Would you like to display 5 rows of raw data? Please type 'yes' or 'no'.\n").strip().lower()
        if display in ['yes', 'yeah', 'y', 'yea', 'yep']:
            if index >= len(df):
                print("No more data to display.\n")
                break
            else:
                print(f"\n{df.iloc[index: index + 5]}\n{'-' * 120}")
                index += 5
        elif display in ['no', 'nah', 'n', 'nope']:
            break
        else:
            print("Invalid input. Please type 'yes' or 'no'.")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
