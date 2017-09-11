# pylint: disable=missing-docstring
from datetime import datetime
from decimal import Decimal
from unittest.mock import patch

import pytz
from django.test import TestCase

from datasource import rates
from datasource.models import candles

SIX_PLACES = Decimal('0.000001')


class RatesImportTest(TestCase):

    @patch.object(rates, 'get_start_date_str', return_value='2017-07-05')
    @patch.object(rates, 'get_end_date_str', return_value='2017-07-10')
    def test_import_rates(self, mock1, mock2):
        # pylint: disable=unused-argument

        # When
        rates.main()
        expected_start_time = datetime(
            2017, 7, 6, 21, tzinfo=pytz.timezone('UTC'))
        expected_high_bid = Decimal(1.29834).quantize(SIX_PLACES)
        expected_close_bid = Decimal(1.29765).quantize(SIX_PLACES)
        expected_open_ask = Decimal(0.9656).quantize(SIX_PLACES)
        expected_low_ask = Decimal(112.836).quantize(SIX_PLACES)

        # Then
        all_candles = candles.get_all(['instrument_id', 'start_time'])
        self.assertEqual(len(all_candles), 20)

        self.assertEqual(all_candles[0].volume, 22237)
        self.assertEqual(all_candles[1].instrument.name, 'EUR_USD')
        self.assertEqual(all_candles[2].start_time, expected_start_time)
        self.assertEqual(all_candles[5].high_bid, expected_high_bid)
        self.assertEqual(all_candles[9].close_bid, expected_close_bid)
        self.assertEqual(all_candles[12].open_ask, expected_open_ask)
        self.assertEqual(all_candles[16].low_ask, expected_low_ask)
