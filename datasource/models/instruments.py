from django.db import models


class Instrument(models.Model):
    name = models.CharField(max_length=10, unique=True, primary_key=True)
    multiplier = models.IntegerField()

    def __str__(self):
        return self.name + ':' + str(self.multiplier)


def get_instrument_by_name(instrument_name):
    return Instrument.objects.get(name=instrument_name)


def get_all():
    return Instrument.objects.all()
