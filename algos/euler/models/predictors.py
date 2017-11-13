""" Data model and data access methods for Predictor for Euler algo.
"""
from django.contrib.postgres.fields import JSONField
from django.db import models


class Predictor(models.Model):
    """ Predictor data model.
    """
    name = models.CharField(max_length=40, unique=True, primary_key=True)
    parameter_range = JSONField()


def create_one(**kwargs):
    """ Create a Predictor object with the given fields.

        Args:
            Named arguments.
                name: Name of the predictor.
                param_range: Dictionary of parameters and their respective
                    range of values. e.g.: {'param_one': [1,2,3]}

        Returns:
            Predictor object with the given fields.
    """
    return Predictor(**kwargs)
