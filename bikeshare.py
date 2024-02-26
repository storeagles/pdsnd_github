import time
import pandas as pd
import numpy as np
import humanize
import os 
import math


CITY_DATA = {"chicago": "chicago.csv",
             "new york city": "new_york_city.csv",
             "washington": "washington.csv"}
MONTHS = ["all", "january", "february", "march", "april", "may", "june",
          "july", "august", "september", "october", "november", "december"]
DAYS_OF_WEEK = ["all", "monday", "tuesday", "wednesday",
                "thursday", "friday", "saturday", "sunday"]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let\"s explore some US bikeshare data!")

    city = None
    month = ""
    day = ""

    while city not in CITY_DATA:
        city = input(
            "please select a city among : " + ", ".join(CITY_DATA.keys()) + " :\n").lower().strip()

    while month not in MONTHS:
        month = input(
            "please select a month among : " + ", ".join(MONTHS) + " :\n").lower().strip()

    while day not in DAYS_OF_WEEK:
        day = input(
            "please select a day among : " + ", ".join(DAYS_OF_WEEK) + " :\n").lower().strip()

    print("-"*40)
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
    # change this line accroding to the relative location of the csv files
    #csv = "./"+CITY_DATA[city]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv = os.path.join(current_dir, CITY_DATA[city])
    df = pd.read_csv(csv, parse_dates=["Start Time", "End Time"])

    if month != "all":
        selected_month = MONTHS.index(month)
        df = df[df["Start Time"].dt.month == selected_month]

    if day != "all":
        selected_date = DAYS_OF_WEEK.index(day) - 1
        df = df[df["Start Time"].dt.dayofweek == selected_date]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()
    column_name = "Start Time"

    df["month"] = df[column_name].dt.month
    df["day_of_week"] = df[column_name].dt.dayofweek
    df["start_hour"] = df[column_name].dt.hour

    month_mode = df["month"].mode()

    if len(month_mode) > 0:
        most_common_month = month_mode[0]
        print("Most common month:", MONTHS[most_common_month+1])

    day_of_week_mode = df["day_of_week"].mode()

    if len(day_of_week_mode) > 0:
        most_common_day_of_week = day_of_week_mode[0]
        print("Most common day of week:",
              DAYS_OF_WEEK[most_common_day_of_week+1])

    start_hour_mode = df["start_hour"].mode()

    if len(start_hour_mode) > 0:
        most_common_start_hour = start_hour_mode[0]
        print("Most common start hour:", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    df["trip"] = df["Start Station"] + " -> " + df["End Station"]

    start_mode = df["Start Station"].mode()
    stop_mode = df["End Station"].mode()
    trip_mode = df["trip"].mode()

    if len(start_mode) > 0:
        most_common_start_station = start_mode[0]
        print("Most commonly used start station:", most_common_start_station)
    if len(stop_mode) > 0:
        most_common_stop_station = [0]
        print("Most commonly used end station:", most_common_stop_station)

    if len(trip_mode) > 0:
        most_common_trip = trip_mode[0]
        print("Most frequent combination of start station and end station trip:",
              most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")

    start_time = time.time()
    column_name = "Trip Duration"

    total_travel_duration = df[column_name].sum()
    mean_travel_duration = df[column_name].mean()

    print("Total travel time :", humanize.precisedelta(total_travel_duration))
    print("Mean travel time :", humanize.precisedelta(mean_travel_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def display_raw_data(df):
    """Displays the raw data content of data frame."""
    print("Showing raw data")

    size = len(df)
    ix = 0
    keep_displaying = True
    page_size = 5

    while (ix < size) & keep_displaying:
        page_end= min(ix+page_size, size-1)
        t = df.iloc[ix:page_end]
        print("Displaying between", ix, "and", page_end,"of total", size, "records.")
        print("-"*40)
        print(t)
        ix += page_size
        keep_displaying = input(
            "\n Would you like to keep displaying raw data? Please respond Yes or No and press enter. \n").lower() == "yes"
        print("-"*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # TO DO: Display counts of user types

    user_types = df.groupby("User Type").size()
    print("Counts of user types :")
    print(user_types)

    if city == "washington":
        print("Gender and Birthday data is not available for the selected city.")
        return
    # TO DO: Display counts of gender

    genders = df.groupby("Gender").size()
    print("Counts of gender :")
    print(genders)

    # TO DO: Display earliest, most recent, and most common year of birth

    column_name = "Birth Year"
    max_birth_year = df[column_name].max()
    most_mode = df[column_name].mode()
    earliest_birth=df[column_name].min(skipna=True)
   
    if math.isnan(earliest_birth) == False :
        earliest_birth_year = int(earliest_birth)
        print("Earliest birth year :", earliest_birth_year)
    
    if len(most_mode) > 0:
        most_common_birth_year = int(most_mode[0])
        print("Most common birth year :", most_common_birth_year)
    
    if math.isnan(max_birth_year) == False :
        most_recent_birth_year = int(max_birth_year)
        print("Most recent birth year :", most_recent_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        show_raw_data = input(
            "\nWould you like to examine the raw data? yes or no\n").lower()
        if show_raw_data == "yes":
            display_raw_data(df)

        restart = input(
            "\nWould you like to restart? Enter yes or no.\n").lower()
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
