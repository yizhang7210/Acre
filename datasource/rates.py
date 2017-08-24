""" This is the datasource.rates module.
    This module is primarily responsible for retriving historical rates from
    a data source, parse them and save them to the database.
    Supported data sources include: OANDA.
"""

# External imports
import datetime

from . import oanda
from .models import candles, instruments


def get_start_date(instrument):
    last_date = candles.get_last(instrument, oanda.Granularity.DAILY.value)
    if last_date is None:
        return '2005-01-02'
    else:
        return str((last_date + datetime.timedelta(1)).date())


def get_end_date():
    return str(datetime.date.today() - datetime.timedelta(1))


def import_daily_candles(oandaConn):
    all_candles = []
    for instrument in instruments.get_all():
        start_date = get_start_date(instrument)
        end_date = get_end_date()

        ocs = oandaConn.get_daily_candles(instrument.name, start_date, end_date)
        all_candles += [oanda.map_candle_to_db(
            oc, instrument.name, oanda.Granularity.DAILY.value) for oc in ocs]

    return all_candles


def main():
    """ Main: Fetch daily candles util yesterday for all instruments.
    """
    oandaConn = oanda.OandaConnection('Game-Dev')
    all_candles = import_daily_candles(oandaConn)
    candles.insert_many(all_candles)

    return


# Main.
if __name__ == "__main__":
    main()
