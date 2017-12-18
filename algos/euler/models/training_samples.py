""" Data model and data access methods for TrainingSample for Euler algo.
"""
from django.contrib.postgres.fields import ArrayField
from django.db import models

from datasource.models.instruments import Instrument


class TrainingSample(models.Model):
    """ TrainingSample data model.
    """
    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.PROTECT
    )
    date = models.DateField()
    features = ArrayField(
        models.DecimalField(max_digits=7, decimal_places=2),
        size=7
    )
    target = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        unique_together = (('instrument', 'date'),)


def create_one(**kwargs):
    """ Create a TrainingSample object with the given fields.

        Args:
            Named arguments.
                instrument: Instrument object.
                date: Date object.
                features: List of Decimals with 2 decimal places.
                target: Decimal with 2 decimal places.

        Returns:
            TrainingSample object with the given fields.
    """
    return TrainingSample(**kwargs)


def get_samples(**kwargs):
    """ Retrieve a list of training samples with given conditions.

        Args:
            kwargs: Named arguments for filtering training samples.
                instrument: Instrument object. Filter by this instrument.
                order_by: String. Space delimited string of fields to order by.
                start: Date object. Filter by samples on or after this date.
                end: Date object. Filter by samples on or before this date.

        Returns:
            List of Candle objects satisfying the conditions (QuerySet).
    """
    samples = TrainingSample.objects.all()
    if kwargs.get('instrument') is not None:
        samples = samples.filter(instrument=kwargs.get('instrument'))
    if kwargs.get('start') is not None:
        samples = samples.filter(date__gte=kwargs.get('start'))
    if kwargs.get('end') is not None:
        samples = samples.filter(date__lte=kwargs.get('end'))
    if kwargs.get('order_by') is not None:
        samples = samples.order_by(kwargs.get('order_by'))

    return samples


def get_all(order_by):
    """ Returns all training samples in the database.

        Args:
            order_by: List of strings to order the samples by.

        Returns:
            List of all TrainingSample objects (QuerySet).
    """
    return TrainingSample.objects.all().order_by(*order_by)


def delete_all():
    """ Delete all training samples in the database.

        Args:
            None.
    """
    return TrainingSample.objects.all().delete()


def get_last(instrument):
    """ Retrieve the latest training sample of given instrument.

        Args:
            instrument: Instrument object.

        Returns:
            TrainingSample object if exists or None.
    """
    samples = TrainingSample.objects.filter(
        instrument=instrument,
    ).order_by('-date')

    if samples:
        return samples[0]


def insert_many(samples):
    """ Bulk insert a list of training samples.

        Args:
            samples: List of TrainingSample objects to be inserted.
    """
    TrainingSample.objects.bulk_create(samples)
