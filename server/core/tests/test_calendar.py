# pylint: disable=missing-docstring
import datetime
from unittest import TestCase

from core import calendar


class CalendarTest(TestCase):

    def test_current_trading_day(self):
        # Weekday before 5pm should be same day
        right_now = datetime.datetime(2017, 12, 5, 13, 35)
        expected = datetime.date(2017, 12, 5)
        self.assertEqual(calendar.get_trading_day(right_now), expected)

        # Weekday after 5pm should be next day
        right_now = datetime.datetime(2017, 12, 5, 18, 5)
        expected = datetime.date(2017, 12, 6)
        self.assertEqual(calendar.get_trading_day(right_now), expected)

        # Friday after 5pm should be Monday
        right_now = datetime.datetime(2017, 12, 15, 20, 35)
        expected = datetime.date(2017, 12, 18)
        self.assertEqual(calendar.get_trading_day(right_now), expected)

        # Saturday and Sunday should all be Monday
        right_now = datetime.datetime(2017, 12, 17, 1, 35)
        expected = datetime.date(2017, 12, 18)
        self.assertEqual(calendar.get_trading_day(right_now), expected)
