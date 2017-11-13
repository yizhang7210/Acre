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
    predictor = models.ForeignKey(
        Predictor,
        on_delete=models.PROTECT
    )
    predictor_params = JSONField()

    class Meta:
        unique_together = (('predictor', 'instrument', 'date'),)
