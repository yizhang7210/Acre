""" This is algos.euler.serializers module.
    This module provides the serializers of the predicted_changes and
    profitable_changes endpoints.
"""
from algos.euler.models.predictions import Prediction
from algos.euler.models.predictors import Predictor
from algos.euler.models.training_samples import TrainingSample
from rest_framework import serializers


class PredictorSerializer(serializers.ModelSerializer):
    """ Serializer of the Predictor model.
    """
    class Meta:
        model = Predictor
        fields = '__all__'


class PredictionSerializer(serializers.ModelSerializer):
    """ Serializer of the Prediction model.
    """
    predicted_change = serializers.FloatField(source='profitable_change')
    predictor = PredictorSerializer()

    class Meta:
        model = Prediction
        fields = ('date', 'instrument', 'predictor', 'predicted_change',
                  'score')


class PriceChangeSerializer(serializers.ModelSerializer):
    """ Serializer of the TrainingSample model for daily profitable change.
    """
    profitable_change = serializers.FloatField(source='target')

    class Meta:
        model = TrainingSample
        fields = ('date', 'instrument', 'profitable_change')
