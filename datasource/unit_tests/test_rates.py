import datetime
from unittest import TestCase
from unittest.mock import patch

from .. import rates
from ..models import candles


class RatesTest(TestCase):
    def test_test_start_date(self):
        # Given
        mock_candle = candles.Candle()
        mock_candle.start_time = datetime.datetime(2017, 5, 3)

        # When
        with patch.object(candles, 'get_last', return_value=mock_candle):
            start_date = rates.get_start_date('DOES NOT MATTER')

        # Then
        self.assertEqual(start_date, '2017-05-05')

        # When
        with patch.object(candles, 'get_last', return_value=candles.Candle()):
            start_date = rates.get_start_date('DOES NOT MATTER')

        # Then
        self.assertEqual(start_date, '2005-01-02')
