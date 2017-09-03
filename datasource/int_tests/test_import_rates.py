from unittest.mock import patch

from django.test import TestCase

from .. import oanda, rates
from ..models import candles, instruments


class RatesImportTest(TestCase):

    @patch.object(rates, 'get_start_date', return_value='2017-07-05')
    @patch.object(rates, 'get_end_date', return_value='2017-07-10')
    def test_import_rates(self, mock1, mock2):

        # When
        rates.main()

        # Then
        all_candles = candles.get_all(['instrument_id', 'start_time'])
        self.assertEqual(20, len(all_candles))

        self.assertEqual(22237, all_candles[0].volume)
        self.assertEqual('EUR_USD', all_candles[1].instrument.name)
        self.assertEqual(1.29171, all_candles[4].open_bid)
        self.assertEqual(1.29834, all_candles[5].high_bid)
        self.assertEqual(1.29268, all_candles[8].low_bid)
        self.assertEqual(1.29765, all_candles[9].close_bid)
        self.assertEqual(0.9656, all_candles[12].open_ask)
        self.assertEqual(0.96612, all_candles[13].high_ask)
        self.assertEqual(112.836, all_candles[16].low_ask)
        self.assertEqual(113.231, all_candles[17].close_ask)
