""" This is algos.api module.
    This module is responsible for the REST API of the algorithms.
"""
from algos import Algos
from algos.euler import views as euler_views
from datasource import Granularity
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class PredictedChangesView(APIView):
    """ Class-based view responsible for the endpoint:
            api/v1/algos/<str:algo>/predicted_changes
    """

    def get(self, request, algo):
        """ GET a list of predicted profitable changes (maximum 200).
            Valid algo names include: euler.

            Filter parameters include:

            - instrument: Name of the trading instrument, e.g. 'EUR_USD'.
            - start: First date of the predictions, e.g. '2017-11-07'.
            - end: Last date of the predictions, e.g. '2017-12-09'
            - order_by: Key to sort the predictions (prefix a minus sign for
                descending), e.g. '-date'. Default is date, ascending.

            For algorithm Euler, each prediction includes:

            - instrument: The traded instrument.
            - date: The trading day of the prediction.
            - predicted_change: How much the rate is predicted to change (in pips).
            - score: A cross validtion score of the prediction. Higher the better.
            - predictor: The machine learning model used for this prediction.
            - predictor_params: The model parameters used for this prediction.
        """
        if algo == Algos.EULER.value:
            return euler_views.get_predicted_changes(request.query_params)

        return Response(
            data={'message': "Specified algo is not supported."},
            status=status.HTTP_404_NOT_FOUND)


class ProfitableChangesView(APIView):
    """ Class-based view responsible for the endpoint:
            api/v1/profitable_changes
    """

    def get(self, request):
        """ GET a list of actual profitable changes (maximum 200).

            Filter parameters include:

            - instrument: Name of the trading instrument, e.g. 'EUR_USD'.
            - granularity: Granularity of the profitable change. Default is 'D'.
            - start: First date of the profitable changes, e.g. '2017-11-07'.
            - end: Last date of the profitable changes, e.g. '2017-12-09'
            - order_by: Key to sort the profitable changes (prefix a minus sign
                for descending), e.g. '-date'. Default is date, ascending.

            Each daily profitable change includes:

            - instrument: The traded instrument.
            - date: The trading day of the profitable change.
            - profitable_change: The amount of profitable price movement for the
                given instrument on the given trading day.
        """
        granularity = request.query_params.get('granularity')
        if granularity is None or granularity == Granularity.DAILY.value:
            return euler_views.get_actual_changes(request.query_params)

        return Response(
            data={'message': "Specified granularity is not supported."},
            status=status.HTTP_404_NOT_FOUND)
