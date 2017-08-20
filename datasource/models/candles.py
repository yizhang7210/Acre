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
