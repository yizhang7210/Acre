""" This is algos.euler.euler module.
    This is the main module for algorithm Euler.
"""

import datetime
import threading

from algos.euler import transformer
from algos.euler.learner import Learner
from algos.euler.models import predictions, predictors
from datasource import Granularity
from datasource.models import candles, instruments


class Euler(threading.Thread):
    """ Euler class. Implements the Euler algorithm"""

    def __init__(self, new_date, **kwargs):
        """ Initialize the Euler class.

            Args:
                new_date: Date object. The date to predict the rate changes.
                Named arguments:
                    cv_fold: Number of folds of cross validation. Default to 10.
        """
        threading.Thread.__init__(self)
        self.prediction_date = new_date
        self.cv_fold = kwargs.get('cv_fold') or 10

    def run(self):
        """ Implements Thread.run. Runs Euler algo's daily update at End-of-Day.

            Args:
                None.

            Returns:
                None.
        """
        transformer.run()
        for ins in instruments.get_all():
            features = self.gather_updated_features(ins)
            self.update_all_prediction(ins, features)

    def gather_updated_features(self, instrument):
        """ Return the features for prediction from the most recent candle.

            Args:
                instrument: Instrument object, for which to predict the rates.

            Returns:
                features: List of Decimals. To be used for prediction.
        """
        yesterday = self.prediction_date - datetime.timedelta(1)
        cutoff_time = datetime.datetime.combine(yesterday, datetime.time())
        last_candle = candles.get_last(
            instrument=instrument,
            granularity=Granularity.DAILY.value,
            before=cutoff_time
        )
        return transformer.extract_features(last_candle)

    def update_all_prediction(self, instrument, features):
        """ Return the list of predictions from all predictors.

            Args:
                instrument: Instrument object, for which to predict the rates.
                features: List of Decimals. To be feed into the learning model.

            Returns:
                None.
        """
        for predictor in predictors.get_all():
            learner = Learner(instrument, predictor)
            learner.learn(before=self.prediction_date, cv_fold=self.cv_fold)
            profitable_change = learner.predict(features)

            predictions.upsert_one(
                instrument=instrument,
                predictor=predictor,
                date=self.prediction_date,
                profitable_change=profitable_change,
                predictor_params=learner.model.get_params()
            )
