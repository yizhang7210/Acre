# pylint: disable=missing-docstring

import datetime

from algos.euler.euler import Euler
from algos.euler.models import training_samples as ts


# To implement RunScript interface.
def run():
    start_date = datetime.date(2006, 1, 1)
    all_dates = []
    for sample in ts.get_samples(start=start_date, order_by='date'):
        all_dates.append(sample.date)

    all_dates = list(set(all_dates))
    all_dates.sort()

    for date in all_dates:
        euler = Euler(date)
        euler.run()
