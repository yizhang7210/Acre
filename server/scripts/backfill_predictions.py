# pylint: disable=missing-docstring

import datetime

from algos.euler.models import training_samples as ts
from algos.euler.runner import Euler


# To implement RunScript interface.
def run(*args):
    if len(args) < 2:
        print("Usage: django-admin runscript backfill_predictions " +
              "--script-args <start-date> <end-date> (e.g. 2018-01-01)")
        return
    start = datetime.datetime.strptime(args[0], '%Y-%m-%d').date()
    end = datetime.datetime.strptime(args[1], '%Y-%m-%d').date()
    all_dates = []
    for sample in ts.get_samples(start=start, end=end, order_by=['date']):
        all_dates.append(sample.date)

    all_dates = list(set(all_dates))
    all_dates.sort()

    for date in all_dates:
        euler = Euler(date)
        euler.run()
