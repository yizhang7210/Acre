# pylint: disable=missing-docstring
import datetime
import math
from decimal import Decimal

from django.test import TestCase

from algos.euler.euler import Euler
from algos.euler.models import training_samples as ts
from algos.euler.models import predictions, predictors
from datasource.models import candles, instruments

from .test_setup import TestSetup

TWO_PLACES = Decimal('0.01')


class EulerAlgoTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(EulerAlgoTest, cls).setUpClass()
        TestSetup.set_up_instruments()
        TestSetup.set_up_candles()
        cls.set_up_predictors()

    @classmethod
    def set_up_predictors(cls):
        param_range = {'max_depth': [3, 4], 'min_samples_split': [2, 3]}
        predictor = predictors.create_one(
            name='treeRegressor', parameter_range=param_range
        )
        predictor.save()

    @classmethod
    def tearDownClass(cls):
        super(EulerAlgoTest, cls).tearDownClass()
        predictors.delete_all()
        predictions.delete_all()
        ts.delete_all()
        candles.delete_all()
        instruments.delete_all()

    def test_euler_end_of_day(self):
        # Given
        today = datetime.date(2017, 12, 6)

        # When
        euler_thread = Euler(today, cv_fold=2)
        euler_thread.run()

        # Then
        new_predictions = predictions.get_all(['date'])
        self.assertEqual(len(new_predictions), 1)
        self.assertEqual(new_predictions[0].date, today)
        self.assertFalse(math.isnan(new_predictions[0].score))
