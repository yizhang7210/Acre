""" This is datasource.views module.
    This module provides the view of the REST API from the data source.
"""
from datasource.models import instruments
from datasource.serializers import InstrumentSerializer
from rest_framework.response import Response


def get_all_instruments():
    """ GET a list of supported trading instruments.
    """
    serializer = InstrumentSerializer(instruments.get_all(), many=True)
    return Response(serializer.data)
