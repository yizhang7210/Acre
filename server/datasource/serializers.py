""" This is datasource.serializers module.
    This module provides the serializers of instruments.
"""
from datasource.models.instruments import Instrument
from rest_framework import serializers


class InstrumentSerializer(serializers.ModelSerializer):
    """ Serializer of the Instrument model.
    """
    class Meta:
        model = Instrument
        fields = '__all__'
