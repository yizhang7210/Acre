""" This is the datasource.oanda module.
    This module is responsible for OANDA related utilities and connections.
"""

# External imports
import http.client
import json
import os
import urllib
from enum import Enum

# Internal imports
from .models import candles, instruments

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
    DAILY = 'D'


class OHLC:
    def __init__(self, ohlc):
        if not ohlc:
            raise TypeError('OHLC requires all of Open, High, Low and Close.')
        if not all(rates in ohlc for rates in ('o', 'h', 'l', 'c')):
            raise TypeError('OHLC requires all of Open, High, Low and Close.')
        self.o = ohlc.get('o')
        self.h = ohlc.get('h')
        self.l = ohlc.get('l')
        self.c = ohlc.get('c')


class OandaCandle:
    def __init__(self, raw_candle):

        if 'time' not in raw_candle or 'complete' not in raw_candle:
            raise TypeError('OANDA Candle missing "complete" and/or "time"')

        self.time = raw_candle.get('time')
        self.complete = raw_candle.get('complete')
        self.volume = raw_candle.get('volume') or 0
        self.ask = OHLC(raw_candle.get('ask')) if 'ask' in raw_candle else None
        self.bid = OHLC(raw_candle.get('bid')) if 'bid' in raw_candle else None
        self.mid = OHLC(raw_candle.get('mid')) if 'mid' in raw_candle else None


class OandaConnection:
    """ The OandaConnection class, responsible for managing HTTP connections
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
            candles = response_content.get('candles')
            return [OandaCandle(x) for x in candles]
        else:
            return []


def map_candle_to_db(oanda_candle, instrument, granularity):
    db_candle = candles.get_empty()

    db_candle.instrument = instruments.get_instrument_by_name(instrument)
    db_candle.granularity = granularity.value
    db_candle.start_time = oanda_candle.time
    db_candle.volume = oanda_candle.volume

    if oanda_candle.bid is not None:
        db_candle.open_bid = oanda_candle.bid.o
        db_candle.high_bid = oanda_candle.bid.h
        db_candle.low_bid = oanda_candle.bid.l
        db_candle.close_bid = oanda_candle.bid.c

    if oanda_candle.ask is not None:
        db_candle.open_ask = oanda_candle.ask.o
        db_candle.high_ask = oanda_candle.ask.h
        db_candle.low_ask = oanda_candle.ask.l
        db_candle.close_ask = oanda_candle.ask.c

    return db_candle
