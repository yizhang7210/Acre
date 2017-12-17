""" This is algos.euler.euler module.
    This is the main module for algorithm Euler.
"""

import threading

from algos.euler import transformer
from algos.euler.learner import Learner
from algos.euler.models import predictions, predictors
from datasource import Granularity
from datasource.models import candles, instruments


class Euler(threading.Thread):
    """ Euler class. Implements the Euler algorithm"""

    def __init__(self, new_date):
        """ Initialize the Euler class.

            Args:
                new_date: Date object. The date to predict the rate changes.
        """
        threading.Thread.__init__(self)
        self.prediction_date = new_date

    def run(self):
        """ Implements Thread.run. Runs Euler algo's daily update at End-of-Day.

            Args:
               None.

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
                    date=self.prediction_date,
                    profitable_change=profitable_change,
                    predictor_params=learner.model.get_params()
                )
                new_prediction.save()
