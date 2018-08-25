import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
global_city='Enter City'
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
    flag=False
    while flag!=True:
        city=input('Which city data would you like to see ? (Chicago / New York City / Washington)\n')
        if city.lower()=='chicago' or city.lower()=='new york city' or city.lower()=='washington':
            flag=True
            global global_city
            global_city=city
            break
        else:
            print('Input City is not valid. Please retry.')
            flag=False
    # TO DO: get user input for month (all, january, february, ... , june)
    flag=False
    while flag!=True:
        month=input('Please enter the month for which you would like to get the details.\n Input the name of month (Note :- Month should be between January to June). Please enter "all" to fetch details for all months\n')
        if month.lower()=='january' or month.lower()=='february' or month.lower()=='march' or month.lower()=='april' or month.lower()=='may' or month.lower()=='june' or month.lower()=='all':
            flag=True
            break
        else:
            print('Input month is not valid. Please retry.')
            flag=False
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    flag=False
    while flag!=True:
        day=input('Please enter the day for which you would like to get the details.\n Input the name of day. Please enter "all" to fetch details for all days\n')
        if day.title()=='Sunday' or day.title()=='Monday' or day.title()=='Tuesday' or day.title()=='Wednesday' or day.title()=='Thursday' or day.title()=='Friday' or day.title()=='Saturday' or day.lower()=='all':
            flag=True
            break
        else:
            print('Entered day is not valid. Please retry.')
            flag=False

    print('-'*40)
    return city.lower(), month.title(), day.title()


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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month.title() != 'All':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
        df = df[df['month'] == month]
    if day.title() != 'All':
        df = df[df['day_of_week']==day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month=df.groupby(['month'])['Start Station'].count().argmax()
    if popular_month==1:
        popular_month='January'
    elif popular_month==2:
        popular_month='February'
    elif popular_month==3:
        popular_month='March'
    elif popular_month==4:
        popular_month='April'
    elif popular_month==5:
        popular_month='May'
    else:
        popular_month='June'
    #Since the file contains data for Jan to June months only 
    print('Most Common Month of Travel is :- {}. '.format(popular_month))
    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day=df.groupby(['day_of_week'])['Start Station'].count().argmax()
    print('Most Common Day of Travel is :- {}.'.format(popular_day))
    
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour=df.groupby(['hour'])['Start Station'].count().argmax()
    print('Most Common Hour of Travel is :- {}00 '.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    # TO DO: display most commonly used end station
    popular_start_station=df.groupby(['Start Station'])['Start Station'].count().argmax()
    popular_end_station=df.groupby(['End Station'])['End Station'].count().argmax()
    print ('Most common start station is {}.\nMost common end station is {}.'.format(popular_start_station,popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    common_trip=df.groupby(['Start Station','End Station'])['Start Station'].count().argmax()
    print ('Most common trip is {} to {}.'.format(common_trip[0],common_trip[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time=df['Trip Duration'].sum()
    mean_travel_time=df['Trip Duration'].mean()
    flag=input('Would you like to get get time details as converted in proper hours and minutes ? (Please type yes/y/Yes for Yes)')
    if flag.lower()=='y' or flag.lower()=='yes' :
        hour,minutes,seconds=convert_seconds(total_travel_time)
        print ('Total Trip Duration is {} seconds which is equal to  {} hours {} minutes and {} seconds.'.format(total_travel_time,hour,minutes,seconds))
    else:
        print ('Total Trip Duration is {} seconds.'.format(total_travel_time))
    # TO DO: display mean travel time
    
    if flag.lower()=='y' or flag.lower()=='yes' :
        hour,minutes,seconds=convert_seconds(mean_travel_time)
        print ('Mean Trip Duration is {} seconds that\'s equal to {} hours {} minutes and {} seconds.'.format(mean_travel_time,hour,minutes,seconds))
    else:
        print ('Mean Trip Duration is {} seconds.'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # TO DO: Display counts of user types
    print(global_city.title())
    
    if global_city.title() == 'Chicago' or global_city.title() == 'New York City':
        # TO DO: Display counts of gender
        count_gender=df.groupby(['Gender'])['Gender'].count()
        print('Counts of Gender \n',count_gender,'\n')
        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_birth_year=df['Birth Year'].min()
        print ('Oldest person travelled have Birth Year {}\n'.format(earliest_birth_year))
        most_recent_birth_year=df['Birth Year'].max()
        print ('Youngest person travelled have Birth Year {}\n'.format(most_recent_birth_year))
        common_birth_year=df.groupby(['Birth Year'])['Birth Year'].count().argmax()
        print('Max People travlled have Birth Year {}.\n'.format(common_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
               
def convert_seconds(seconds):
    temp=seconds
    hour=(seconds-(seconds%3600))/3600
    temp=temp-(hour*3600)
    seconds=temp
    minutes=(seconds-(seconds%60))/60
    temp=temp-(minutes*60)
    seconds=temp
    return hour,minutes,seconds

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        restart = input('\nWould you like to restart? Enter yes/y or n/no.\n')
        if restart.lower()=='yes' or restart.lower()=='y':
            True
        else:
            False
            break

if __name__ == "__main__":
	main()
