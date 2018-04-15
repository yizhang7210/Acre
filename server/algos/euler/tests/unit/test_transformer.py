# pylint: disable=missing-docstring
import datetime
from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch

from algos.euler import transformer as tsfr
from algos.euler.models import training_samples as ts
from core.models import instruments
from datasource.models import candles

TWO_PLACES = Decimal('0.01')


class TransformerTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.set_up_instruments()
        cls.set_up_candles()

    @classmethod
    def set_up_instruments(cls):
        cls.eur_usd = instruments.Instrument()
        cls.eur_usd.name = 'EUR_USD'
        cls.eur_usd.multiplier = 10000

        cls.usd_jpy = instruments.Instrument()
        cls.usd_jpy.name = 'USD_JPY'
        cls.usd_jpy.multiplier = 100

    @classmethod
    def set_up_candles(cls):
        # EUR_USD 1
        bid = {'o': 1.29288, 'h': 1.29945, 'l': 1.29045, 'c': 1.29455}
        ask = {'o': 1.29343, 'h': 1.29967, 'l': 1.29063, 'c': 1.29563}
        cls.candle_eur_usd = candles.create_one(bid=bid, ask=ask)
        cls.candle_eur_usd.instrument = cls.eur_usd

        # EUR_USD 2
        bid = {'o': 1.29455, 'h': 1.29878, 'l': 1.29045, 'c': 1.29521}
        ask = {'o': 1.29563, 'h': 1.29902, 'l': 1.29056, 'c': 1.29533}
        cls.candle_eur_usd_2 = candles.create_one(bid=bid, ask=ask)
        cls.candle_eur_usd_2.instrument = cls.eur_usd
        cls.candle_eur_usd_2.start_time = datetime.datetime(2017, 9, 7, 17)

        # USD_JPY
        bid = {'o': 109.954, 'h': 110.470, 'l': 109.557, 'c': 109.213}
        ask = {'o': 110.025, 'h': 110.519, 'l': 109.571, 'c': 109.299}
        cls.candle_usd_jpy = candles.create_one(bid=bid, ask=ask)
        cls.candle_usd_jpy.instrument = cls.usd_jpy

    def test_extract_features(self):
        # When
        features = tsfr.extract_features(self.candle_eur_usd)
        expected = [65.7, -24.3, 16.7, 5.5, 67.9, -22.5, 27.5]
        expected = [Decimal(x).quantize(TWO_PLACES) for x in expected]

        # Then
        self.assertEqual(features, expected)

        # When
        features = tsfr.extract_features(self.candle_usd_jpy)
        expected = [51.6, -39.7, -74.1, 7.1, 56.5, -38.3, -65.5]
        expected = [Decimal(x).quantize(TWO_PLACES) for x in expected]

        # Then
        self.assertEqual(features, expected)

    def test_get_profitable_change(self):
        # When
        profitable_change = tsfr.get_profitable_change(self.candle_eur_usd)
        expected = Decimal(10000 * (1.29455 - 1.29343)).quantize(TWO_PLACES)

        # Then
        self.assertEqual(profitable_change, expected)

        # When
        profitable_change = tsfr.get_profitable_change(self.candle_usd_jpy)
        expected = Decimal(100 * (109.299 - 109.954)).quantize(TWO_PLACES)

        # Then
        self.assertEqual(profitable_change, expected)

    def test_build_training_sample(self):
        # When
        sample = tsfr.build_sample_row(
            self.candle_eur_usd, self.candle_eur_usd_2)

        # Then
        expected_fs = [65.7, -24.3, 16.7, 5.5, 67.9, -22.5, 27.5]
        expected_fs = [Decimal(x).quantize(TWO_PLACES) for x in expected_fs]
        self.assertEqual(sample.instrument, self.eur_usd)
        self.assertEqual(sample.date, datetime.date(2017, 9, 8))
        self.assertEqual(sample.features, expected_fs)
        self.assertEqual(sample.target, 0)

    def test_start_time(self):
        # Given
        mock_sample = ts.create_one(date=datetime.date(2017, 5, 3))

        # When - Then
        expected = datetime.datetime(2017, 5, 2)
        with patch.object(ts, 'get_last', return_value=mock_sample):
            self.assertEqual(tsfr.get_start_time('DOES NOT MATTER'), expected)

        # When - Then
        expected = datetime.datetime(2005, 1, 1)
        with patch.object(ts, 'get_last', return_value=None):
            self.assertEqual(tsfr.get_start_time('DOES NOT MATTER'), expected)
