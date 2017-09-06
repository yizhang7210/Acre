from unittest import TestCase
from unittest.mock import patch

from datasource import oanda
from datasource.models import instruments


class OandaTest(TestCase):

    def test_ohlc_instantiation(self):
        # Incomplete
        with self.assertRaises(TypeError):
            oanda.OHLC(None)

        # Incomplete
        with self.assertRaises(TypeError):
            oanda.OHLC({'o': 1, 'h': 2, 'l': 0.5})

        # Success
        input_ohlc = {'o': 1, 'h': 2, 'l': 0.5, 'c': 1.2}
        ohlc = oanda.OHLC(input_ohlc)
        self.assertEqual(ohlc.o, input_ohlc.get('o'))
        self.assertEqual(ohlc.h, input_ohlc.get('h'))
        self.assertEqual(ohlc.l, input_ohlc.get('l'))
        self.assertEqual(ohlc.c, input_ohlc.get('c'))

    def test_oanda_candle_instantiation(self):
        # Incomplete
        with self.assertRaises(TypeError):
            oanda.OandaCandle()

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
            'time': '2015-11-23',
            'complete': True,
            'volume': 3456,
            'ask': {'o': 3.4, 'h': 4.1, 'l': 2.3, 'c': 4}
        }
        oc = oanda.OandaCandle(complete_candle)
        self.assertEqual(oc.time, complete_candle.get('time'))
        self.assertEqual(oc.volume, complete_candle.get('volume'))
        self.assertEqual(oc.ask.o, complete_candle.get('ask').get('o'))
        self.assertIsNone(oc.bid)

    def test_oanda_connection_instantiation(self):
        # Invalid
        with self.assertRaises(TypeError):
            oanda.OandaConnection('InvalidEnvironment')

        # Game
        oConn = oanda.OandaConnection(oanda.GAME)
        self.assertEqual(oConn.url, oanda.GAME_URL)
        self.assertEqual(oConn.access_token, oanda.GAME_TOKEN)
        self.assertIsNotNone(oConn.conn)

    def test_map_to_db_with_valid_instrument(self):
        # Given
        raw_candle = {
            'time': '2015-11-23',
            'complete': True,
            'volume': 3456,
            'ask': {'o': 3.4, 'h': 4.1, 'l': 2.3, 'c': 4}
        }
        oc = oanda.OandaCandle(raw_candle)
        mock_instrument = instruments.Instrument()
        mock_instrument.name = 'GBP_USD'

        # When
        gran = oanda.Granularity.DAILY
        with patch.object(instruments, 'get_instrument_by_name',
                          return_value=mock_instrument):
            db_candle = oanda.map_candle_to_db(oc, 'DOES NOT MATTER', gran)

        # Then
        self.assertEqual(db_candle.instrument.name, 'GBP_USD')
        self.assertEqual(db_candle.granularity, gran.value)
        self.assertEqual(db_candle.start_time, oc.time)
        self.assertEqual(db_candle.high_ask, oc.ask.h)
