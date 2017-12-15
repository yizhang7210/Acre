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

def create_one(**kwargs):
    """ Create an Instrument object with the given fields.

        Args:
            Named arguments.
                name: String. Name of the instrument.
                multiplier: Integer. The pip multiplier of the instrument.

        Returns:
            Instrument object with the given fields.
    """
    return Instrument(**kwargs)

def delete_all():
    """ Delete all instruments in the database.

        Args:
            None.
    """
    return Instrument.objects.all().delete()

def insert_many(instruments):
    """ Bulk insert a list of instruments.

        Args:
            instruments: List of Instrument objects to be inserted.
    """
    Instrument.objects.bulk_create(instruments)
