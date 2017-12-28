""" This is algos.euler.views module.
    This module provides the view of the REST API from the Euler algo.
"""
from algos.euler.models import training_samples as ts
from algos.euler.models import predictions
from algos.euler.serializers import PredictionSerializer, PriceChangeSerializer
from rest_framework.response import Response


def get_predicted_changes(query_params):
    """ Get a list of predicted profitable changes (maximum 200).
    """
    all_predictions = predictions.get_predictions(
        instrument=query_params.get('instrument'),
        start=query_params.get('start'),
        end=query_params.get('end'),
        order_by=query_params.get('order_by') or 'date')
    serializer = PredictionSerializer(all_predictions[:200], many=True)
    return Response(serializer.data)


def get_actual_changes(query_params):
    """ Get a list of actual profitable changes (maximum 200).
    """
    all_changes = ts.get_samples(
        instrument=query_params.get('instrument'),
        start=query_params.get('start'),
        end=query_params.get('end'),
        order_by=query_params.get('order_by') or 'date')
    serializer = PriceChangeSerializer(all_changes[:200], many=True)
    return Response(serializer.data)
