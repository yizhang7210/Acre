""" This is algos.api module.
    This module is responsible for the REST API of the algorithms.
"""
import datetime

from algos import Algos, calendar
from algos.euler import views as euler_views
from algos.euler.runner import Euler
from datasource import views as datasource_views
from datasource import rates
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


class InstrumentsView(APIView):
    """ List all supported trading instruments.
    """

    def get(self, request):
        """ GET a list of all supported trading instruments.
        """
        return datasource_views.get_all_instruments()


class PredictedChangesView(APIView):
    """ Predicted profitable changes for a given period of time.
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
            - limit: Number of predictions to limit the reponse by (max 200).

            For algorithm Euler, each prediction includes:

            - instrument: The traded instrument.
            - date: The trading day of the prediction.
            - predicted_change: How much the rate is predicted to change (in pips).
            - score: A cross validtion score of the prediction. Higher the better.
            - predictor: The machine learning model used for this prediction.
            - predictor_params: The model parameters used for this prediction.
        """
        algo_view = get_algo_view(algo)
        if algo_view is not None:
            return algo_view.get_predicted_changes(request.query_params)

        return Response(
            data={'message': "Specified algo is not supported."},
            status=status.HTTP_404_NOT_FOUND)


class ProfitableChangesView(APIView):
    """ Actual profitable changes for a given period of time.
    """

    def get(self, request, algo):
        """ GET a list of actual profitable changes (maximum 200).
            Valid algo names include: euler.

            Filter parameters include:

            - instrument: Name of the trading instrument, e.g. 'EUR_USD'.
            - start: First date of the profitable changes, e.g. '2017-11-07'.
            - end: Last date of the profitable changes, e.g. '2017-12-09'
            - order_by: Key to sort the profitable changes (prefix a minus sign
                for descending), e.g. '-date'. Default is date, ascending.
            - limit: Number of changes to limit the reponse by (max 200).

            For algorithm Euler, each daily profitable change includes:

            - instrument: The traded instrument.
            - date: The trading day of the profitable change.
            - profitable_change: The amount of profitable price movement for the
                given instrument on the given trading day.
        """
        algo_view = get_algo_view(algo)
        if algo_view is not None:
            return algo_view.get_actual_changes(request.query_params)

        return Response(
            data={'message': "Specified algo is not supported."},
            status=status.HTTP_404_NOT_FOUND)


def get_algo_view(algo):
    """ Return the specific API view of the given algorithm.

        Args:
            algo: String. Name of the predictive algorithm.

        Returns:
            an APIView that can handle the corresponding request for the algo.
    """
    if algo == Algos.EULER.value:
        return euler_views


@api_view(['GET'])
def get_all_algos(request):
    # pylint: disable=unused-argument
    """ List all supported algorithms.
    """
    return Response([{'name': 'Euler', 'description': 'One day auto-regression.'}])


@api_view(['GET'])
def get_current_trading_day(request):
    # pylint: disable=unused-argument
    """ Return the date string of current trading day.
    """
    now = timezone.now()
    date = calendar.get_trading_day(now)
    return Response({'date': date.isoformat()})


@require_POST
@csrf_exempt
def end_of_day_update(request):
    # pylint: disable=unused-argument
    """ Main entry point for all algos."""
    if calendar.is_week_day(datetime.date.today()):
        run_end_of_day()
    return HttpResponse('OK')


def run_end_of_day():
    """ The actual process of End-of-Day update"""
    day_to_predict = calendar.get_trading_day(datetime.datetime.now())
    rates.run()
    euler_thread = Euler(day_to_predict)
    euler_thread.start()
