""" This is algos.euler.transformer module.
    This module is responsible for transforming raw candle data into training
    samples usable to the Euler algorithm.
"""
import datetime
import decimal

from algos.euler.models import training_samples as ts
from datasource.models import candles, instruments

TWO_PLACES = decimal.Decimal('0.01')


def extract_features(day_candle):
    """ Extract the features for the learning algorithm from a daily candle.
        The Features are:
            high_bid, low_bid, close_bid, open_ask, high_ask, low_ask,
            and close_ask (all relative to open_bid) in pips.

        Args:
            day_candle: candles.Candle object representing a daily candle.

        Returns:
            features: List of Decimals. The features described above, all in two
                decimal places.
    """
    multiplier = day_candle.instrument.multiplier
    features = [
        day_candle.high_bid,
        day_candle.low_bid,
        day_candle.close_bid,
        day_candle.open_ask,
        day_candle.high_ask,
        day_candle.low_ask,
        day_candle.close_ask,
    ]
    features = [multiplier * (x - day_candle.open_bid) for x in features]
    features = [decimal.Decimal(x).quantize(TWO_PLACES) for x in features]

    return features


def get_profitable_change(day_candle):
    """ Get the potential daily profitable price change in pips.
            If prices rise enough, we have: close_bid - open_ask (> 0), buy.
            If prices fall enough, we have: close_ask - open_bid (< 0), sell.
            if prices stay relatively still, we don't buy or sell. It's 0.

        Args:
            day_candle: candles.Candle object representing a daily candle.

        Returns:
            profitable_change: Decimal. The profitable rate change described
                above, in two decimal places.
    """
    multiplier = day_candle.instrument.multiplier
    change = 0
    if day_candle.close_bid > day_candle.open_ask:
        change = multiplier * (day_candle.close_bid - day_candle.open_ask)
    elif day_candle.close_ask < day_candle.open_bid:
        change = multiplier * (day_candle.close_ask - day_candle.open_bid)

    return decimal.Decimal(change).quantize(TWO_PLACES)


def build_sample_row(candle_previous, candle_next):
    """ Build one training sample from two consecutive days of candles.

        Args:
            candle_previous: candles.Candle object. Candle of first day.
            candle_next: candles.Candle object. Candle of second day.

        Returns:
            sample: TrainingSample object. One training sample for learning.
    """
    return ts.create_one(
        instrument=candle_next.instrument,
        date=candle_next.start_time.date() + datetime.timedelta(1),
        features=extract_features(candle_previous),
        target=get_profitable_change(candle_next))


def get_start_time(instrument):
    """ Get the start time for retrieving candles of the given instrument.
        This is determined by the last training sample in the database.

        Args:
            instrument: Instrument object. The given instrument.

        Returns:
            start_time: Datetime object. The datetime from which to query
                candles from to fill the rest of the training samples.
    """
    last_sample = ts.get_last(instrument)
    if last_sample is not None:
        start_date = last_sample.date - datetime.timedelta(1)
        return datetime.datetime.combine(start_date, datetime.time())

    return datetime.datetime(2005, 1, 1)


def run():
    """ Update the training samples in the database from the latest candles.
        This should be run daily to ensure the training set is up-to-date.

        Args:
            None.
    """
    all_new_samples = []
    for instrument in instruments.get_all():
        start_time = get_start_time(instrument)
        new_candles = candles.get_candles(
            instrument=instrument, start=start_time, order_by='start_time')
        for i in range(len(new_candles) - 1):
            all_new_samples.append(
                build_sample_row(new_candles[i], new_candles[i + 1]))

    ts.insert_many(all_new_samples)
