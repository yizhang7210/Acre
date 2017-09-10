""" Data model and data access methods for Instrument.
"""
from django.db import models


class Instrument(models.Model):
    """ Instrument data model.
    """
    name = models.CharField(max_length=10, unique=True, primary_key=True)
    multiplier = models.IntegerField()

    def __str__(self):
        return self.name + ':' + str(self.multiplier)


def get_instrument_by_name(instrument_name):
    """ Returns the instrument with the given name.

        Args:
            instrument_name: String. Name of the instrument.

        Returns:
            Instrument object.
    """

    return Instrument.objects.get(name=instrument_name)


def get_all():
    """ Returns all instruments in the database.

        Args:
            None.

        Returns:
            List of Instrument objects (QuerySet).
    """
    return Instrument.objects.all()
