""" Data model and data access methods for Predictor for Euler algo.
"""
from django.contrib.postgres.fields import JSONField
from django.db import models


class Predictor(models.Model):
    """ Predictor data model.
    """
    name = models.CharField(max_length=40, unique=True, primary_key=True)
    parameters = JSONField(default={})


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


def get_all():
    """ Returns all predictors in the database.

        Args:
            None.

        Returns:
            List of Predictor objects (QuerySet).
    """
    return Predictor.objects.all()


def delete_all():
    """ Delete all predictors in the database.

        Args:
            None.
    """
    return Predictor.objects.all().delete()


def insert_many(predictors):
    """ Bulk insert a list of predictors.

        Args:
            predictors: List of Predictor objects to be inserted.
    """
    Predictor.objects.bulk_create(predictors)
