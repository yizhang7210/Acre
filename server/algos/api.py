""" This is algos.api module.
    This module is responsible for the REST API of the algorithms.
"""
import datetime

from algos import Algos, calendar
from algos.euler import views as euler_views
from algos.euler.runner import Euler
from datasource import views as datasource_views
from datasource import Granularity, rates
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


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


class InstrumentsView(APIView):
    """ List supported trading instruments.
    """

    def get(self, request):
        """ GET a list of supported trading instruments.
        """
        return datasource_views.get_all_instruments()


class ProfitableChangesView(APIView):
    """ Actual profitable changes for a given period of time.
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
