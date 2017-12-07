# pylint: disable=missing-docstring
import datetime
from decimal import Decimal

from django.test import TestCase

from algos.euler import euler
from algos.euler.models import predictions, predictors
from datasource.models import candles, instruments

TWO_PLACES = Decimal('0.01')


class EulerAlgoTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(EulerAlgoTest, cls).setUpClass()
        cls.set_up_instruments()
        cls.set_up_candles()
        cls.set_up_predictors()

    @classmethod
    def set_up_instruments(cls):
        cls.eur_usd = instruments.Instrument(name='EUR_USD', multiplier=10000)
        cls.eur_usd.save()

    @classmethod
    def set_up_candles(cls):
        bid = {'o': 1.29288, 'h': 1.29945, 'l': 1.29045, 'c': 1.29455}
        ask = {'o': 1.29343, 'h': 1.29967, 'l': 1.29063, 'c': 1.29563}
        day_one = candles.create_one(
            bid=bid, ask=ask,
            instrument=cls.eur_usd,
            start_time=datetime.datetime(2017, 9, 4, 17),
            volume=5,
            granularity='D'
        )
        day_one.save()

    @classmethod
    def set_up_predictors(cls):
        param_range = {'max_depth': [3, 4], 'min_samples_split': [5, 10]}
        predictor = predictors.create_one(
            name='treeRegressor', parameter_range=param_range
        )
        predictor.save()

    @classmethod
    def tearDownClass(cls):
        super(EulerAlgoTest, cls).tearDownClass()
        candles.delete_all()
        predictors.delete_all()
        predictions.delete_all()

    def test_euler_end_of_day(self):

        # Given
        today = datetime.date(2017, 12, 6)

        # When
        euler.on_end_of_day_update(today)

        # Then
        self.assertEqual(1, 1)
