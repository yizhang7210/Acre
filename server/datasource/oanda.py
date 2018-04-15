""" This is the datasource.oanda module.
    This module is responsible for OANDA related utilities and connections.
"""

import http.client
import json
import os
import urllib
from datetime import datetime
from decimal import Decimal
from enum import Enum

import pytz
from core.models import instruments
from datasource import Granularity
from datasource.models import candles

SIX_PLACES = Decimal('0.000001')

# OANDA constants
GAME_URL = "api-fxpractice.oanda.com"
TRADE_URL = "api-fxtrade.oanda.com"

GAME_TOKEN = os.environ.get('TOKEN_GAME')
TRADE_TOKEN = os.environ.get('TOKEN_TRADE')


class Env(Enum):
    """ OANDA Env. Can be either GAME or TRADE
    """
    GAME = 'Game'
    TRADE = 'Trade'


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

        self.time = parse_time_str(raw_candle.get('time'))
        self.complete = raw_candle.get('complete')
        self.volume = raw_candle.get('volume') or 0
        self.ask = raw_candle.get('ask') if 'ask' in raw_candle else None
        self.bid = raw_candle.get('bid') if 'bid' in raw_candle else None
        self.mid = raw_candle.get('mid') if 'mid' in raw_candle else None


class OandaConnection:
    """ The OandaConnection class, responsible for managing HTTPS connections
        with OANDA.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, environment):
        """ Initialize the OandaConnection class with existing account.

            Args:
                environment: Env. One of Env.GAME or Env.TRADE.
        """
        if environment == Env.GAME:
            self.url = GAME_URL
            self.access_token = GAME_TOKEN
        elif environment == Env.TRADE:
            self.url = TRADE_URL
            self.access_token = TRADE_TOKEN
        else:
            raise TypeError('Environment has to be Env.GAME or Env.TRADE')

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
    db_candle = candles.create_one(
        instrument=instruments.get_instrument_by_name(instrument),
        granularity=granularity.value,
        start_time=oanda_candle.time,
        volume=oanda_candle.volume,
        bid=to_decimal(oanda_candle.bid),
        ask=to_decimal(oanda_candle.ask)
    )

    return db_candle


def parse_time_str(time_str):
    """ Parse an RFC3339 time stamp to datetime object in UTC.

        Args:
            time_str: String. Timestamp. e.g. 2017-07-04T21:00:00.000000000Z

        Returns:
            Datetime object with the given time in UTC.
    """
    time = datetime.strptime(time_str[:-4], '%Y-%m-%dT%H:%M:%S.%f')
    time = time.replace(tzinfo=pytz.timezone('UTC'))

    return time


def to_decimal(ohlc):
    """ Convert the content of a dictionary (ohlc) to decimal with 6 places.

        Args:
            ohlc: Dictionary.

        Returns:
            Same dictionary with its values converted to Deicmals.
    """
    if ohlc is None:
        return
    for key in ohlc:
        ohlc[key] = Decimal(ohlc.get(key)).quantize(SIX_PLACES)

    return ohlc
