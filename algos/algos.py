""" This is algos module.
    This module is the entry point for all algorithms.
"""
import datetime

from django_cron import CronJobBase, Schedule

from algos import calendar
from algos.euler.euler import Euler
from datasource import rates


class AcreAlgos(CronJobBase):
    """ The entry point of all algorithms in Acre"""
    schedule = Schedule(run_at_times=['17:01'])
    code = 'all_acre_algos'

    #pylint: disable=no-self-use
    def do(self):
        """ Implementing the CronJobBase base class/interface."""
        if calendar.is_week_day(datetime.date.today()):
            run_end_of_day()

def run_end_of_day():
    """ The actual process of End-of-Day update"""
    day_to_predict = calendar.get_trading_day(datetime.datetime.now())
    rates.main()
    euler_thread = Euler(day_to_predict)
    euler_thread.start()
