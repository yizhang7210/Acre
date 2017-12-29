# pylint: disable=missing-docstring
from datetime import datetime
from decimal import Decimal
from unittest.mock import patch

import pytz
from django.test import TestCase

from datasource import rates
from datasource.models import candles, instruments

SIX_PLACES = Decimal('0.000001')


class RatesImportTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(RatesImportTest, cls).setUpClass()
        eur_usd = instruments.Instrument(name='EUR_USD', multiplier=10000)
        eur_usd.save()
        usd_jpy = instruments.Instrument(name='USD_JPY', multiplier=100)
        usd_jpy.save()

    @classmethod
    def tearDownClass(cls):
        super(RatesImportTest, cls).tearDownClass()
        candles.delete_all()
        instruments.delete_all()

    @patch.object(rates, 'get_start_date_str', return_value='2017-07-05')
    @patch.object(rates, 'get_end_date_str', return_value='2017-07-10')
    def test_import_rates(self, mock1, mock2):
        # pylint: disable=unused-argument

        # When
        rates.run()
        expected_start_time = datetime(
            2017, 7, 6, 21, tzinfo=pytz.timezone('UTC'))
        expected_low_ask = Decimal(1.13823).quantize(SIX_PLACES)
        expected_high_bid = Decimal(114.172).quantize(SIX_PLACES)

        # Then
        all_candles = candles.get_all(['instrument_id', 'start_time'])
        self.assertEqual(len(all_candles), 8)

        self.assertEqual(all_candles[0].volume, 22237)
        self.assertEqual(all_candles[1].instrument.name, 'EUR_USD')
        self.assertEqual(all_candles[2].start_time, expected_start_time)
        self.assertEqual(all_candles[3].low_ask, expected_low_ask)
        self.assertEqual(all_candles[6].high_bid, expected_high_bid)
