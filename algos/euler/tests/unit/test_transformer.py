import datetime
from unittest import TestCase
from unittest.mock import patch

import numpy as np

from algos.euler.models import training_samples as ts
from algos.euler.transformer import Transformer
from datasource.models import candles, instruments


class TransformerTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.setUpInstruments()
        cls.setUpCandles()

    @classmethod
    def setUpInstruments(cls):
        cls.eur_usd = instruments.Instrument()
        cls.eur_usd.name = 'EUR_USD'
        cls.eur_usd.multiplier = 10000

        cls.usd_jpy = instruments.Instrument()
        cls.usd_jpy.name = 'USD_JPY'
        cls.usd_jpy.multiplier = 100

    @classmethod
    def setUpCandles(cls):
        # EUR_USD 1
        bid = {'o': 1.29288, 'h': 1.29945, 'l': 1.29045, 'c': 1.29455}
        ask = {'o': 1.29343, 'h': 1.29967, 'l': 1.29063, 'c': 1.29563}
        cls.candle_eur_usd = candles.get_one(bid=bid, ask=ask)
        cls.candle_eur_usd.instrument = cls.eur_usd

        # EUR_USD 2
        bid = {'o': 1.29455, 'h': 1.29878, 'l': 1.29045, 'c': 1.29521}
        ask = {'o': 1.29563, 'h': 1.29902, 'l': 1.29056, 'c': 1.29533}
        cls.candle_eur_usd_2 = candles.get_one(bid=bid, ask=ask)
        cls.candle_eur_usd_2.instrument = cls.eur_usd
        cls.candle_eur_usd_2.start_time = datetime.datetime(2017, 9, 7, 17)

        # USD_JPY
        bid = {'o': 109.954, 'h': 110.470, 'l': 109.557, 'c': 109.213}
        ask = {'o': 110.025, 'h': 110.519, 'l': 109.571, 'c': 109.299}
        cls.candle_usd_jpy = candles.get_one(bid=bid, ask=ask)
        cls.candle_usd_jpy.instrument = cls.usd_jpy

    def test_extract_features(self):
        t = Transformer()
        # When
        features = t.extract_features(self.candle_eur_usd)
        expected = [65.7, -24.3, 16.7, 5.5, 67.9, -22.5, 27.5]

        # Then
        np.testing.assert_almost_equal(features, expected, decimal=2)

        # When
        features = t.extract_features(self.candle_usd_jpy)
        expected = [51.6, -39.7, -74.1, 7.1, 56.5, -38.3, -65.5]

        # Then
        np.testing.assert_almost_equal(features, expected, decimal=2)

    def test_get_profitable_change(self):
        t = Transformer()
        # When
        profitable_change = t.get_profitable_change(self.candle_eur_usd)
        expected = 10000 * (1.29455 - 1.29343)

        # Then
        np.testing.assert_almost_equal(profitable_change, expected, decimal=2)

        # When
        profitable_change = t.get_profitable_change(self.candle_usd_jpy)
        expected = 100 * (109.299 - 109.954)

        # Then
        np.testing.assert_almost_equal(profitable_change, expected, decimal=2)

    def test_build_training_sample(self):
        t = Transformer()
        # When
        sample = t.build_sample_row(self.candle_eur_usd, self.candle_eur_usd_2)

        # Then
        expected_fs = [65.7, -24.3, 16.7, 5.5, 67.9, -22.5, 27.5]
        self.assertEqual(sample.instrument, self.eur_usd)
        self.assertEqual(sample.date, datetime.date(2017, 9, 8))
        np.testing.assert_almost_equal(sample.features, expected_fs, decimal=2)
        self.assertEqual(sample.target, 0)

    def test_start_time(self):
        t = Transformer()
        # Given
        mock_sample = ts.TrainingSample()
        mock_sample.date = datetime.date(2017, 5, 3)

        # When - Then
        expected = datetime.datetime(2017, 5, 2)
        with patch.object(ts, 'get_last', return_value=mock_sample):
            self.assertEqual(t.get_start_time('DOES NOT MATTER'), expected)

        # When - Then
        expected = datetime.datetime(2005, 1, 1)
        with patch.object(ts, 'get_last', return_value=None):
            self.assertEqual(t.get_start_time('DOES NOT MATTER'), expected)
