import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
INVALID_INPUT = "Invalid input, please try again..."
POSSIBLE_MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
POSSIBLE_DAYS = ['all', 'saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']

has_month_filter = False
has_day_filter = False

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    month = None
    day = None
    while True:
        try:
            city = input("Cities: New York City, Washington, Chicago\nEnter the name of the city you would like to observe: ").lower().strip()
            if(city in CITY_DATA):
                break
            else:
                print(INVALID_INPUT)
        except:
            print(INVALID_INPUT)

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("\nEnter the name of the month you would like to filter by (a month between january and june or 'all'): ").lower().strip()
            if(month in POSSIBLE_MONTHS):
                break
            else:
                print(INVALID_INPUT)
        except:
            print(INVALID_INPUT)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("\nEnter the name of the day you would like to filter by (Saturday, Sunday etc. or 'all'): ").lower().strip()
            if(day in POSSIBLE_DAYS):
                break
            else:
                print(INVALID_INPUT)
        except:
            print(INVALID_INPUT)

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
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        global has_month_filter
        has_month_filter = True
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        global has_day_filter
        has_day_filter = True
        # filter by day of week to create the new dataframe
        df = df[df['Day of week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel in the chosen dataset."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month if there has been no month filter
    if has_month_filter == False:
        popular_month = df['Month'].mode()[0]
        print("The most popular month is: {}".format(POSSIBLE_MONTHS[popular_month].title()))
    # display the most common day of week
    if has_day_filter == False:
        popular_day = df['Day of week'].mode()[0]
        print("The most popular day is: {}".format(popular_day))
    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Hour'].mode()[0]
    print("The most popular hour is: {}".format(popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_end = df['End Station'].mode()[0]
    print("The most popular end station is: {}".format(popular_end))

    # display most commonly used end station
    popular_start = df['Start Station'].mode()[0]
    print("The most popular start station is: {}".format(popular_start))
    # display most frequent combination of start station and end station trip
    df['Combination'] = df['Start Station'] + " -> " + df['End Station']
    popular_combo = df['Combination'].mode()[0]
    print("The most popular start station is: {}".format(popular_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_hours = (df['Trip Duration'].sum() / 60) / 60
    print("The total number of hours spent biking is: {}".format(total_hours))
    # display mean travel time
    mean_minutes = df['Trip Duration'].mean() / 60
    print("The average number of minutes spent biking is: {}".format(mean_minutes))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    subscriber_count = len(df[df['User Type'] == 'Subscriber'])
    customer_count = len(df[df['User Type'] == 'Customer'])
    print("Number of Subscribers: {}\nNumber of Customers: {}".format(subscriber_count, customer_count))

    if 'Gender' in df.columns and 'Birth Year' in df.columns:
        # Display counts of gender
        male_count = len(df[df['Gender'] == 'Male'])
        female_count = len(df[df['Gender'] == 'Female'])
        print("Number of Males: {}\nNumber of Females: {}".format(male_count, female_count))
        # Display earliest, most recent, and most common year of birth
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print("Earliest birth year: {}\nMost recent birth year: {}\nMost commmon birth year: {}".format(earliest_year, recent_year, common_year))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        # initialise row index
        index = 0
        # execute while the next 5 rows doesn't exceed the maximum number of rows
        while index < (df.shape[0] - 5):
            print('\n5 Pieces of Sample Data:')
            # print the next 5 rows
            for i in range(5):
                print('\n')
                print(df.iloc[index])
                print('\n')
                index += 1
            print_more = input('\nWould you like to see more raw data? Enter yes or no.\n')
            if print_more.lower().strip() != 'yes':
                break
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower().strip() != 'yes':
            break


if __name__ == "__main__":
	main()
