# pylint: disable=missing-docstring

import datetime

from algos.euler.models import training_samples as ts
from algos.euler.runner import Euler


# To implement RunScript interface.
def run():
    start = datetime.date(2017, 11, 1)
    end = datetime.date(2017, 12, 24)
    all_dates = []
    for sample in ts.get_samples(start=start, end=end, order_by=['date']):
        all_dates.append(sample.date)

    all_dates = list(set(all_dates))
    all_dates.sort()

    for date in all_dates:
        euler = Euler(date)
        euler.run()
