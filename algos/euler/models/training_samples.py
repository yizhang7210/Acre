from django.contrib.postgres.fields import ArrayField
from django.db import models

from datasource.models.instruments import Instrument


class TrainingSample(models.Model):
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


def get_one(**kwargs):
    return TrainingSample(**kwargs)


def get_all(sortBy):
    return TrainingSample.objects.all().order_by(*sortBy)


def get_last(instrument):
    samples = TrainingSample.objects.filter(
        instrument=instrument,
    ).order_by('-date')

    if(len(samples) > 0):
        return samples[0]
    else:
        return None


def insert_many(samples):
    TrainingSample.objects.bulk_create(samples)
