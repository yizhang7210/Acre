# pylint: disable=missing-docstring
import datetime
from decimal import Decimal

from algos.euler import transformer as tsfr
from algos.euler.models import training_samples as ts
from core.models import instruments
from datasource.models import candles
from django.test import TestCase

from .test_setup import TestSetup

TWO_PLACES = Decimal('0.01')


class TransformationTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TransformationTest, cls).setUpClass()
        TestSetup.set_up_instruments()
        TestSetup.set_up_candles()

    @classmethod
    def tearDownClass(cls):
        super(TransformationTest, cls).tearDownClass()
        ts.delete_all()
        candles.delete_all()
        instruments.delete_all()

    def test_training_data_transform(self):
        # When
        tsfr.run()

        # Then
        samples = ts.get_all(['date'])
        self.assertEqual(len(samples), 3)
        self.assertEqual(samples[1].date, datetime.date(2017, 9, 6))
        self.assertEqual(samples[2].target, Decimal(-5.9).quantize(TWO_PLACES))
