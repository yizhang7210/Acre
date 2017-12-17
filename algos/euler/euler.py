""" This is algos.euler.euler module.
    This is the main module for algorithm Euler.
"""

from algos.euler import transformer
from algos.euler.learner import Learner
from algos.euler.models import predictions, predictors
from datasource import Granularity
from datasource.models import candles, instruments


def on_end_of_day_update(new_date):
    """ Euler algo's daily update at End-of-Day.

        Args:
            new_date: Date object. The next trade date that just started.

        Returns:
            None.
    """
    transformer.run()
    for ins in instruments.get_all():
        last_candle = candles.get_last(ins, Granularity.DAILY.value)
        if not last_candle:
            return
        features = transformer.extract_features(last_candle)
        for predictor in predictors.get_all():
            learner = Learner(ins, predictor)
            learner.learn()
            profitable_change = learner.predict(features)

            new_prediction = predictions.create_one(
                instrument=ins,
                predictor=predictor,
                date=new_date,
                profitable_change=profitable_change,
                predictor_params=learner.model.get_params()
            )
            new_prediction.save()
