""" Data model and data access methods for Candles.
"""
import pytz
from django.db import models

from .instruments import Instrument


class Candle(models.Model):
    """ Candle data model.
    """
    # pylint: disable=too-many-instance-attributes

    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.PROTECT
    )
    start_time = models.DateTimeField()
    volume = models.PositiveIntegerField()

    granularity = models.CharField(max_length=5)

    open_bid = models.DecimalField(max_digits=12, decimal_places=6)
    high_bid = models.DecimalField(max_digits=12, decimal_places=6)
    low_bid = models.DecimalField(max_digits=12, decimal_places=6)
    close_bid = models.DecimalField(max_digits=12, decimal_places=6)

    open_ask = models.DecimalField(max_digits=12, decimal_places=6)
    high_ask = models.DecimalField(max_digits=12, decimal_places=6)
    low_ask = models.DecimalField(max_digits=12, decimal_places=6)
    close_ask = models.DecimalField(max_digits=12, decimal_places=6)

    class Meta:
        unique_together = (('instrument', 'start_time', 'granularity'),)


def get_empty():
    """ Returns an empty Candle object.
    """
    return Candle()


def create_one(**kwargs):
    """ Create a Candle object with the given fields.
    """
    if 'bid' in kwargs:
        bid = kwargs.get('bid')
        del kwargs['bid']
        if bid is not None:
            kwargs['open_bid'] = bid.get('o')
            kwargs['high_bid'] = bid.get('h')
            kwargs['low_bid'] = bid.get('l')
            kwargs['close_bid'] = bid.get('c')

    if 'ask' in kwargs:
        ask = kwargs.get('ask')
        del kwargs['ask']
        if ask is not None:
            kwargs['open_ask'] = ask.get('o')
            kwargs['high_ask'] = ask.get('h')
            kwargs['low_ask'] = ask.get('l')
            kwargs['close_ask'] = ask.get('c')

    if 'start_time' in kwargs:
        kwargs['start_time'] = add_timezone(kwargs.get('start_time'))

    return Candle(**kwargs)


def get_all(order_by):
    """ Returns all candles in the database.

        Args:
            order_by: List of strings to order the candles by.

        Returns:
            List of all Candle objects (QuerySet).
    """
    return Candle.objects.all().order_by(*order_by)


def get_candles(**kwargs):
    """ Retrieve a list of candles with given conditions.

        Args:
            kwargs: Named arguments for filtering candles.
                instrument: Instrument object. Filter by this instrument.
                start: Datetime. Filter candles with later time than 'start'.
                order_by: String. Space delimited string of fields to order by.

        Returns:
            List of Candle objects satisfying the conditions (QuerySet).
    """
    candles = Candle.objects.all()
    if 'instrument' in kwargs:
        candles = candles.filter(instrument=kwargs.get('instrument'))
    if 'start' in kwargs:
        start_time = add_timezone(kwargs.get('start'))
        candles = candles.filter(start_time__gte=start_time)
    if 'order_by' in kwargs:
        candles = candles.order_by(kwargs.get('order_by'))

    return candles


def get_last(instrument, granularity):
    """ Retrieve the latest candle of given instrument and granularity.

        Args:
            instrument: Instrument object.
            granularity: String. The granularity of the candles.

        Returns:
            Candle object if exists or None.
    """
    candles = Candle.objects.filter(
        instrument=instrument,
        granularity=granularity
    ).order_by('-start_time')

    if candles:
        return candles[0]


def add_timezone(time_record):
    """ Add a default America/New_York timezone info to a datetime object.

        Args:
            time_record: Datetime object.

        Returns:
            Datetime object with a timezone if time_record did not have tzinfo,
            otherwise return time_record itself.
    """
    if time_record.tzname() is None:
        return time_record.replace(tzinfo=pytz.timezone('America/New_York'))

    return time_record


def insert_many(candles):
    """ Bulk insert a list of candles.

        Args:
            candles: List of Candle objects to be inserted.
    """
    Candle.objects.bulk_create(candles)
