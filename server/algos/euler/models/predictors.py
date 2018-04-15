""" Data model and data access methods for Predictor for Euler algo.
"""
from django.contrib.postgres.fields import JSONField
from django.db import models


class Predictor(models.Model):
    """ Predictor data model.
    """
    name = models.CharField(max_length=40, unique=True, primary_key=True)
    parameters = JSONField(default={})
    is_active = models.BooleanField(default=False)


def create_one(**kwargs):
    """ Create a Predictor object with the given fields.

        Args:
            Named arguments.
                name: Name of the predictor.
                parameters: Dictionary of parameters e.g. {'param_one': 3}
                is_active: Boolean. Whether this predictor is actively used.

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


def get_active():
    """ Returns the one active predictors in the database.

        Args:
            None.

        Returns:
            A single active Predictor.
    """
    return Predictor.objects.get(is_active=True)


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
