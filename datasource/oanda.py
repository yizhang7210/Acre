""" This is the datasource.oanda module.
    This module is responsible for OANDA related utilities and connections.
"""

import http.client
import json
import os
import urllib
from decimal import Decimal
from enum import Enum

from .models import candles, instruments

SIX_PLACES = Decimal('0.000001')

# Account Details.
APP_DIR = os.path.dirname(os.path.realpath(__file__))
ACCOUNT_INFO = json.load(open('{0}/credentials.json'.format(APP_DIR), 'r'))

GAME = 'Game'
GAME_URL = "api-fxpractice.oanda.com"
GAME_TOKEN = ACCOUNT_INFO.get('Token-Game')

TRADE = 'Trade'
TRADE_URL = "api-fxtrade.oanda.com"
TRADE_TOKEN = ACCOUNT_INFO.get('Token-Trade')


class Granularity(Enum):
    """ Granularity Enum class. Currently only support DAILY.
    """
    DAILY = 'D'


class OHLC:
    """ The OHLC class records the open, high, low and close.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, ohlc):
        """ Initialize the OHLC class with a dictionary.

            Args:
                ohlc: Dictionary. Need to contain keys 'o', 'h', 'l', 'c'.
        """
        if not ohlc:
            raise TypeError('OHLC requires all of Open, High, Low and Close.')
        if not all(rates in ohlc for rates in ('o', 'h', 'l', 'c')):
            raise TypeError('OHLC requires all of Open, High, Low and Close.')
        self.o = ohlc.get('o')
        self.h = ohlc.get('h')
        self.l = ohlc.get('l')
        self.c = ohlc.get('c')


class OandaCandle:
    """ The OandaCandle class represents a candle returned form OANDA's API.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, raw_candle):
        """ Initialize the OandaCandle class with a dictionary.

            Args:
                raw_candle: Dictionary. Need to contain 'time' and 'complete'.
                    May also contain 'volume', 'bid', 'ask', and 'mid'.
        """

        if 'time' not in raw_candle or 'complete' not in raw_candle:
            raise TypeError('OANDA Candle missing "complete" and/or "time"')

        self.time = raw_candle.get('time')
        self.complete = raw_candle.get('complete')
        self.volume = raw_candle.get('volume') or 0
        self.ask = OHLC(raw_candle.get('ask')) if 'ask' in raw_candle else None
        self.bid = OHLC(raw_candle.get('bid')) if 'bid' in raw_candle else None
        self.mid = OHLC(raw_candle.get('mid')) if 'mid' in raw_candle else None


class OandaConnection:
    """ The OandaConnection class, responsible for managing HTTPS connections
        with OANDA.
    """

    def __init__(self, environment):
        """ Initialize the OandaConnection class with existing account.

            Args:
                environment: String. One of oanda.GAME or oanda.TRADE.
        """
        if environment == GAME:
            self.url = GAME_URL
            self.access_token = GAME_TOKEN
        elif environment == TRADE:
            self.url = TRADE_URL
            self.access_token = TRADE_TOKEN
        else:
            raise TypeError('Environment has to be oanda.GAME or oanda.TRADE')

        self.conn = http.client.HTTPSConnection(self.url)
        self.headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer {0}".format(self.access_token)
        }

        return

    def get_environment(self):
        """ Returns the environment of the connection, either GAME or TRADE.

            Args:
                None.

            Returns:
                String. oanda.GAME for game, or oanda.TRADE for trade.
        """
        if self.url == GAME_URL:
            return GAME
        elif self.url == TRADE_URL:
            return TRADE

    def fetch_daily_candles(self, instrument, start_date, end_date):
        """ Obtain a list of daily bid-ask candles for the given instrument.
            Candles are from start_date to end_date, both inclusive. Non-trading
            days will be skipped. Candles are aligned according to New York time
            at 17:00.

            Args:
                instrument: String. The currency pair. e.g. 'EUR_USD'.
                start_date: String. Formatted start date. e.g. '2015-11-24'.
                end_date: Sting. Formatted end date. e.g. '2015-11-28'.

            Returns:
                candles: List of OandaCandle's. See OandaCandle for details.
        """
        date_suffix = "T00:00:00Z"
        query_params = {
            'from': start_date + date_suffix,
            'to': end_date + date_suffix,
            'price': 'BA',
            'granularity': Granularity.DAILY.value,
            'dailyAlignment': 17,
            'alignmentTimezone': 'America/New_York',
        }
        url = ("/v3/instruments/{0}/candles?{1}").format(
            instrument,
            urllib.parse.urlencode(query_params)
        )

        self.conn.request("GET", url, "", self.headers)
        response = self.conn.getresponse()
        response_content = json.loads(response.read().decode())
        self.conn.close()

        if 'candles' in response_content:
            daily_candles = response_content.get('candles')
            return [OandaCandle(x) for x in daily_candles]

        return []


def map_candle_to_db(oanda_candle, instrument, granularity):
    """ Map a OandaCandle to a candles.Candle object.

        Args:
            oanda_candle: OandaCandle object.
            instrument: String. The currency pair. e.g. 'EUR_USD'.
            granularity: Granularity object.

        Returns:
            db_candle: candles.Candle object with the given info.
    """
    db_candle = candles.get_empty()

    db_candle.instrument = instruments.get_instrument_by_name(instrument)
    db_candle.granularity = granularity.value
    db_candle.start_time = oanda_candle.time
    db_candle.volume = oanda_candle.volume

    if oanda_candle.bid is not None:
        db_candle.open_bid = Decimal(oanda_candle.bid.o).quantize(SIX_PLACES)
        db_candle.high_bid = Decimal(oanda_candle.bid.h).quantize(SIX_PLACES)
        db_candle.low_bid = Decimal(oanda_candle.bid.l).quantize(SIX_PLACES)
        db_candle.close_bid = Decimal(oanda_candle.bid.c).quantize(SIX_PLACES)

    if oanda_candle.ask is not None:
        db_candle.open_ask = Decimal(oanda_candle.ask.o).quantize(SIX_PLACES)
        db_candle.high_ask = Decimal(oanda_candle.ask.h).quantize(SIX_PLACES)
        db_candle.low_ask = Decimal(oanda_candle.ask.l).quantize(SIX_PLACES)
        db_candle.close_ask = Decimal(oanda_candle.ask.c).quantize(SIX_PLACES)

    return db_candle
