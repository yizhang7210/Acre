"""Acre URL Configuration
"""
from algos import algos, api
from django.urls import path
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path('algos', algos.main),
    path('api/v1/profitable_changes', api.ProfitableChangesView.as_view()),
    path('api/v1/algos/<str:algo>/predicted_changes',
         api.PredictedChangesView.as_view()),
    path('api/v1/docs/', get_swagger_view(title='Acre API'))
]
