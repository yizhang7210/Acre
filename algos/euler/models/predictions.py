""" Data model and data access methods for Prediction for Euler algo.
"""
from django.contrib.postgres.fields import JSONField
from django.db import models

from datasource.models.instruments import Instrument

from .predictors import Predictor


class Prediction(models.Model):
    """ Prediction data model.
    """
    date = models.DateField()
    profitable_change = models.DecimalField(max_digits=7, decimal_places=2)
    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.PROTECT
    )
    score = models.FloatField()
    predictor = models.ForeignKey(
        Predictor,
        on_delete=models.PROTECT
    )
    predictor_params = JSONField()

    class Meta:
        unique_together = (('predictor', 'instrument', 'date'),)

def create_one(**kwargs):
    """ Create a Prediction object with the given fields.

        Args:
            Named arguments.
                date: Date object. Date of the predicted changes.
                profitable_change: Decimal. Predicted profitable change in pips.
                instrument: Instrument object.
                score: Float. The cross validation score of this prediction.
                predictor: Predictor object.
                predictor_params: Dict. Parameters used for this prediction.

        Returns:
            Predicton object with the given fields.
    """
    return Prediction(**kwargs)

def get_all(order_by):
    """ Returns all predictions in the database.

        Args:
            order_by: List of strings to order the predictions by.

        Returns:
            List of all Prediction objects (QuerySet).
    """
    return Prediction.objects.all().order_by(*order_by)

def delete_all():
    """ Delete all predictions in the database.

        Args:
            None.
    """
    return Prediction.objects.all().delete()

def insert_many(predictions):
    """ Bulk insert a list of predictions.

        Args:
            predictions: List of Prediction objects to be inserted.
    """
    Prediction.objects.bulk_create(predictions)

def upsert(prediction):
    """ Insert or update a prediction.

        Args:
            prediction: Prediction Object to be upserted according to the unique
                together constraint on date, instrument and predictor.

        Returns:
            None.
    """
    existing = Prediction.objects.filter(
        date=prediction.date,
        instrument=prediction.instrument,
        predictor=prediction.predictor
    )
    if existing:
        existing = existing[0]
        existing.profitable_change = prediction.profitable_change
        existing.predictor_params = prediction.predictor_params
        existing.save()
    else:
        prediction.save()
