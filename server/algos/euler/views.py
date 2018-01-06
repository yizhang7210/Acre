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
    order = query_params.get('order_by')
    if order is not None:
        order = order.split(',')
    else:
        order = ['date']
    all_predictions = predictions.get_predictions(
        instrument=query_params.get('instrument'),
        start=query_params.get('start'),
        end=query_params.get('end'),
        order_by=order)
    limit = query_params.get('limit')
    if limit is None or int(limit) > 200:
        limit = 200
    else:
        limit = int(limit)
    serializer = PredictionSerializer(all_predictions[:limit], many=True)
    return Response(serializer.data)


def get_actual_changes(query_params):
    """ Get a list of actual profitable changes (maximum 200).
    """
    order = query_params.get('order_by')
    if order is not None:
        order = order.split(',')
    else:
        order = ['date']

    all_changes = ts.get_samples(
        instrument=query_params.get('instrument'),
        start=query_params.get('start'),
        end=query_params.get('end'),
        order_by=order)
    limit = query_params.get('limit')
    if limit is None or int(limit) > 200:
        limit = 200
    else:
        limit = int(limit)
    serializer = PriceChangeSerializer(all_changes[:limit], many=True)
    return Response(serializer.data)


def clean_predictions():
    """ Clean up predictions made by Euler for a non trading day.
    """
    all_dates = []
    for sample in ts.get_all(['date']):
        all_dates.append(sample.date)

    all_dates = list(set(all_dates))
    all_dates.sort()

    last_day = all_dates[-1]

    predictions.Prediction.objects.filter(date__lte=last_day).exclude(
        date__in=all_dates).delete()
