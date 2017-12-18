""" This is the datasource.rates module.
    This module is primarily responsible for retriving historical rates from
    a data source, parse them and save them to the database.
    Supported data sources include: OANDA.
"""

import datetime

from datasource import Granularity, oanda
from datasource.models import candles, instruments


def get_start_date_str(instrument):
    """ Figure out the last daily candle of the given instrument and hence the
        start date for fetching new ones.

        Args:
            instrument: instruments.Instrument object.

        Returns:
            start_date: String. Formatted start date. e.g. '2015-09-08'
    """
    last_candle = candles.get_last(
        instrument=instrument,
        granularity=Granularity.DAILY.value
    )
    if last_candle is not None:
        last_date = last_candle.start_time
        # Candles are aligned with America/New_York time.
        # Hence a candle with start_time of 2017-08-06 is really for the 7th.
        return str((last_date + datetime.timedelta(2)).date())

    return '2005-01-02'


def get_end_date_str():
    """ Returns the current date - 1 as the last day to retrive the candles.

        Args:
            None.

        Returns:
            end_date: String. Formatted end date. e.g. '2015-09-08'
    """
    return str(datetime.date.today() - datetime.timedelta(1))


def import_daily_candles(conn):
    """ Retrieve daily candles given a connection object for all existing
        instruments in the database.

        Args:
            conn: OandaConnection object.

        Returns:
            all_candles: List of candles.Candle objects. Retrieved candles.
    """
    all_candles = []
    for instrument in instruments.get_all():
        start_date = get_start_date_str(instrument)
        end_date = get_end_date_str()

        ocs = conn.fetch_daily_candles(instrument.name, start_date, end_date)
        all_candles += [oanda.map_candle_to_db(
            oc, instrument.name, Granularity.DAILY) for oc in ocs]

    return all_candles


def main():
    """ Main: Fetch daily candles util yesterday for all instruments.
    """
    oanda_conn = oanda.OandaConnection(oanda.GAME)
    all_candles = import_daily_candles(oanda_conn)
    candles.insert_many(all_candles)

    return
