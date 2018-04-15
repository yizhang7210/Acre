""" This is core.calendar module.
    This module is responsible for calendar related utilities.
"""
import datetime

import pytz


def is_week_day(the_date):
    """ Decides if the given date is a weekday.

        Args:
            the_date: Date object. The date to decide.

        Returns:
            Boolean. Whether the given date is a weekday.
    """
    return the_date.isoweekday() in [1, 2, 3, 4, 5]


def get_next_weekday(the_date):
    """ Returns the date of next weekday following the given date.

        Args:
            the_date: Date object. The given date.

        Returns:
            Date object. Date of the next weekday following the given date.
    """
    if the_date.isoweekday() == 5:
        return the_date + datetime.timedelta(3)
    elif the_date.isoweekday() == 6:
        return the_date + datetime.timedelta(2)

    return the_date + datetime.timedelta(1)


def get_trading_day(given_time):
    """ Returns the trading day of the given time.

        Args:
            given_time: Datetime object. If it does not have a timezone, default
                to America/New York.

        Returns:
            Date object. The date of trading day of the given time.
    """
    new_york_time = pytz.timezone('America/New_York')
    if given_time.tzname() is None:
        given_time = given_time.replace(tzinfo=new_york_time)

    given_time = given_time.astimezone(new_york_time)

    if is_week_day(given_time.date()) and \
            given_time.time() < datetime.time(17, 0, 0):
        return given_time.date()

    return get_next_weekday(given_time.date())
