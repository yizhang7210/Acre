from django.db import models

from .instruments import Instrument


class Candle(models.Model):
    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.PROTECT
    )
    start_time = models.DateTimeField()
    volume = models.PositiveIntegerField()

    granularity = models.CharField(max_length=5)

    open_bid = models.FloatField()
    high_bid = models.FloatField()
    low_bid = models.FloatField()
    close_bid = models.FloatField()

    open_ask = models.FloatField()
    high_ask = models.FloatField()
    low_ask = models.FloatField()
    close_ask = models.FloatField()

    class Meta:
        unique_together = (('instrument', 'start_time', 'granularity'),)


def get_empty():
    return Candle()


def get_one(**kwargs):
    if 'bid' in kwargs:
        bid = kwargs.get('bid')
        kwargs['open_bid'] = bid.get('o')
        kwargs['high_bid'] = bid.get('h')
        kwargs['low_bid'] = bid.get('l')
        kwargs['close_bid'] = bid.get('c')
        del kwargs['bid']

    if 'ask' in kwargs:
        ask = kwargs.get('ask')
        kwargs['open_ask'] = ask.get('o')
        kwargs['high_ask'] = ask.get('h')
        kwargs['low_ask'] = ask.get('l')
        kwargs['close_ask'] = ask.get('c')
        del kwargs['ask']

    return Candle(**kwargs)


def get_all(sortBy):
    return Candle.objects.all().order_by(*sortBy)


def get_candles(**kwargs):
    candles = Candle.objects.all()
    if 'instrument' in kwargs:
        candles = candles.filter(instrument=kwargs.get('instrument'))
    if 'start' in kwargs:
        candles = candles.filter(start_time__gte=kwargs.get('start'))
    if 'sortBy' in kwargs:
        candles = candles.order_by(kwargs.get('sortBy'))

    return candles


def get_last(instrument, granularity):
    candles = Candle.objects.filter(
        instrument=instrument,
        granularity=granularity
    ).order_by('-start_time')

    if(len(candles) > 0):
        return candles[0]
    else:
        return None


def insert_many(candles):
    Candle.objects.bulk_create(candles)
