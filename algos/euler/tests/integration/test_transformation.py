import datetime

import numpy as np
from django.test import TestCase

from algos.euler.models import training_samples as ts
from algos.euler.transformer import Transformer
from datasource.models import candles, instruments


class TransformationTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TransformationTest, cls).setUpClass()
        cls.setUpInstruments()
        cls.setUpCandles()
        cls.setUpSamples()

    @classmethod
    def setUpInstruments(cls):
        cls.eur_usd = instruments.Instrument(name='EUR_USD', multiplier=10000)
        cls.eur_usd.save()

    @classmethod
    def setUpCandles(cls):
        # EUR_USD 1
        bid = {'o': 1.29288, 'h': 1.29945, 'l': 1.29045, 'c': 1.29455}
        ask = {'o': 1.29343, 'h': 1.29967, 'l': 1.29063, 'c': 1.29563}
        day_one = candles.get_one(
            bid=bid, ask=ask,
            instrument=cls.eur_usd,
            start_time=datetime.datetime(2017, 9, 4, 17),
            volume=5
        )

        # EUR_USD 2
        bid = {'o': 1.29455, 'h': 1.29878, 'l': 1.29045, 'c': 1.29521}
        ask = {'o': 1.29563, 'h': 1.29902, 'l': 1.29056, 'c': 1.29533}
        day_two = candles.get_one(
            bid=bid, ask=ask,
            instrument=cls.eur_usd,
            start_time=datetime.datetime(2017, 9, 5, 17),
            volume=5
        )

        # EUR_USD 3
        bid = {'o': 1.29521, 'h': 1.29678, 'l': 1.29345, 'c': 1.29444}
        ask = {'o': 1.29533, 'h': 1.29702, 'l': 1.29356, 'c': 1.29462}
        day_three = candles.get_one(
            bid=bid, ask=ask,
            instrument=cls.eur_usd,
            start_time=datetime.datetime(2017, 9, 6, 17),
            volume=5
        )

        candles.insert_many([day_one, day_two, day_three])

    @classmethod
    def setUpSamples(cls):
        sample = ts.TrainingSample(
            instrument=cls.eur_usd,
            date=datetime.date(2017, 9, 6),
            features=([0] * 7),
            target=0
        )
        sample.save()

    def test_training_data_transformation(self):
        # When
        t = Transformer()
        t.run()

        # Then
        samples = ts.get_all(['date'])
        self.assertEqual(len(samples), 2)
        self.assertEqual(samples[1].date, datetime.date(2017, 9, 7))
        np.testing.assert_almost_equal(samples[1].target, -5.9, decimal=2)
