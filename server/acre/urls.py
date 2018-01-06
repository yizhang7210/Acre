"""Acre URL Configuration
"""
from algos import api
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

api_v1_patterns = [
    path('docs/', get_swagger_view(title='Acre API')),
    path('instruments', api.InstrumentsView.as_view()),
    path('trading_day/current', api.get_current_trading_day),
    path('algos', api.get_all_algos),
    path('algos/update/end_of_day', api.end_of_day_update),
    path('algos/update/clean', api.clean_predictions),
    path('algos/<str:algo>/profitable_changes',
         api.ProfitableChangesView.as_view()),
    path('algos/<str:algo>/predicted_changes',
         api.PredictedChangesView.as_view()),
]

urlpatterns = [
    path('v1/', include(api_v1_patterns)),
]
