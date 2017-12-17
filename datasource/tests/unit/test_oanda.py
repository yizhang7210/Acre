# pylint: disable=missing-docstring
from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch

from datasource import Granularity, oanda
from datasource.models import instruments

SIX_PLACES = Decimal('0.000001')


class OandaTest(TestCase):

    def test_oanda_candle_instantiation(self):
        # Incomplete
        with self.assertRaises(TypeError):
            oanda.OandaCandle(None)

        # Incomplete
        incomplete_candle = {'time': '2018-09-12'}
        with self.assertRaises(TypeError):
            oanda.OandaCandle(incomplete_candle)

        # Incomplete
        incomplete_candle = {'complete': False}
        with self.assertRaises(TypeError):
            oanda.OandaCandle(incomplete_candle)

        # Success
        complete_candle = {
            'time': '2015-11-23T21:00:00.000000000Z',
            'complete': True,
            'volume': 3456,
            'ask': {'o': 3.4, 'h': 4.1, 'l': 2.3, 'c': 4}
        }
        oc = oanda.OandaCandle(complete_candle)
        self.assertEqual(oc.time.day, 23)
        self.assertEqual(oc.volume, complete_candle.get('volume'))
        self.assertEqual(oc.ask.get('o'), complete_candle.get('ask').get('o'))
        self.assertIsNone(oc.bid)

    def test_oanda_conn_instantiation(self):
        # Invalid
        with self.assertRaises(TypeError):
            oanda.OandaConnection('InvalidEnvironment')

        # Game
        oanda_conn = oanda.OandaConnection(oanda.GAME)
        self.assertEqual(oanda_conn.url, oanda.GAME_URL)
        self.assertEqual(oanda_conn.access_token, oanda.GAME_TOKEN)
        self.assertIsNotNone(oanda_conn.conn)

    def test_map_to_candles_to_db(self):
        # Given
        raw_candle = {
            'time': '2015-11-24T21:00:00.000000000Z',
            'complete': True,
            'volume': 3456,
            'ask': {'o': 3.4, 'h': 4.1, 'l': 2.3, 'c': 4}
        }
        oc = oanda.OandaCandle(raw_candle)
        mock_instrument = instruments.Instrument()
        mock_instrument.name = 'GBP_USD'

        # When
        gran = Granularity.DAILY
        with patch.object(instruments, 'get_instrument_by_name',
                          return_value=mock_instrument):
            db_candle = oanda.map_candle_to_db(oc, 'DOES NOT MATTER', gran)

        # Then
        self.assertEqual(db_candle.instrument.name, 'GBP_USD')
        self.assertEqual(db_candle.granularity, gran.value)
        self.assertEqual(db_candle.start_time, oc.time)
        expected_high_ask = Decimal(oc.ask.get('h')).quantize(SIX_PLACES)
        self.assertEqual(db_candle.high_ask, expected_high_ask)
