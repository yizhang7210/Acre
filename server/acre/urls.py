"""Acre URL Configuration
"""
from api import views as api_views
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

api_v1_patterns = [
    path('docs/', get_swagger_view(title='Acre API')),
    path('instruments', api_views.InstrumentsView.as_view()),
    path('trading_day/current', api_views.get_current_trading_day),
    path('algos', api_views.get_all_algos),
    path('algos/update/end_of_day', api_views.end_of_day_update),
    path('algos/update/clean', api_views.clean_predictions),
    path('algos/<str:algo>/profitable_changes',
         api_views.ProfitableChangesView.as_view()),
    path('algos/<str:algo>/predicted_changes',
         api_views.PredictedChangesView.as_view()),
]

urlpatterns = [
    path('v1/', include(api_v1_patterns)),
]
