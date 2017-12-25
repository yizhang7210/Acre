""" This is algos module.
    This module is the entry point for all algorithms.
"""
import datetime

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from algos import calendar
from algos.euler.euler import Euler
from datasource import rates


@require_POST
@csrf_exempt
def main(request):
    """ Main entry point for all algos."""
    if calendar.is_week_day(datetime.date.today()):
        run_end_of_day()
    return HttpResponse('OK')

def run_end_of_day():
    """ The actual process of End-of-Day update"""
    day_to_predict = calendar.get_trading_day(datetime.datetime.now())
    rates.main()
    euler_thread = Euler(day_to_predict)
    euler_thread.start()
