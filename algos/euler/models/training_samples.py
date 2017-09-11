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
    """ Create a Candle object with the given fields.
    """
    return TrainingSample(**kwargs)


def get_all(order_by):
    """ Returns all training samples in the database.

        Args:
            order_by: List of strings to order the samples by.

        Returns:
            List of all TrainingSample objects (QuerySet).
    """
    return TrainingSample.objects.all().order_by(*order_by)


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
