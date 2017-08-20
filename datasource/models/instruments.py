from django.db import models


class Instrument(models.Model):
    name = models.CharField(max_length=10, unique=True, primary_key=True)
    multiplier = models.IntegerField()
