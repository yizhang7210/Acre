""" This is algos.main module.
    This module is the entry point for all algorithms.
"""
import datetime

from celery import shared_task

from algos.euler.euler import Euler
from datasource import rates


@shared_task
def main():
    """ Entry point."""
    today = datetime.date.today()
    rates.main()
    euler_thread = Euler(today)
    euler_thread.start()
