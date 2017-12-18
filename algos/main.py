""" This is algos.main module.
    This module is the entry point for all algorithms.
"""
import datetime

from celery import shared_task

from algos import calendar
from algos.euler.euler import Euler
from datasource import rates


@shared_task
def main():
    """ Entry point."""
    if calendar.is_week_day(datetime.date.today()):
        run_end_of_day()

def run_end_of_day():
    """ The actual process of End-of-Day update"""
    day_to_predict = calendar.get_trading_day(datetime.datetime.now())
    rates.main()
    euler_thread = Euler(day_to_predict)
    euler_thread.start()
