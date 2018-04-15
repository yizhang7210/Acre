# pylint: disable=missing-docstring
import datetime

from core.models import instruments
from datasource.models import candles


class TestSetup():
    @classmethod
    def set_up_instruments(cls):
        cls.eur_usd = instruments.Instrument(name='EUR_USD', multiplier=10000)
        cls.eur_usd.save()

    @classmethod
    def set_up_candles(cls):
        # EUR_USD 1
        bid = {'o': 1.29845, 'h': 1.30001, 'l': 1.29222, 'c': 1.29288}
        ask = {'o': 1.29863, 'h': 1.30027, 'l': 1.29235, 'c': 1.29343}
        day_one = candles.create_one(
            bid=bid, ask=ask,
            instrument=cls.eur_usd,
            start_time=datetime.datetime(2017, 9, 3, 17),
            granularity='D',
            volume=8
        )

        # EUR_USD 2
        bid = {'o': 1.29288, 'h': 1.29945, 'l': 1.29045, 'c': 1.29455}
        ask = {'o': 1.29343, 'h': 1.29967, 'l': 1.29063, 'c': 1.29563}
        day_two = candles.create_one(
            bid=bid, ask=ask,
            instrument=cls.eur_usd,
            start_time=datetime.datetime(2017, 9, 4, 17),
            granularity='D',
            volume=5
        )

        # EUR_USD 3
        bid = {'o': 1.29455, 'h': 1.29878, 'l': 1.29045, 'c': 1.29521}
        ask = {'o': 1.29563, 'h': 1.29902, 'l': 1.29056, 'c': 1.29533}
        day_three = candles.create_one(
            bid=bid, ask=ask,
            instrument=cls.eur_usd,
            start_time=datetime.datetime(2017, 9, 5, 17),
            granularity='D',
            volume=5
        )

        # EUR_USD 4
        bid = {'o': 1.29521, 'h': 1.29678, 'l': 1.29345, 'c': 1.29444}
        ask = {'o': 1.29533, 'h': 1.29702, 'l': 1.29356, 'c': 1.29462}
        day_four = candles.create_one(
            bid=bid, ask=ask,
            instrument=cls.eur_usd,
            start_time=datetime.datetime(2017, 9, 6, 17),
            granularity='D',
            volume=5
        )

        candles.insert_many([day_one, day_two, day_three, day_four])
