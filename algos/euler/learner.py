""" This is algos.euler.learner module.
    This module is responsible for training the models and make predictions.
"""
import datetime
import decimal
import itertools

import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor

from algos.euler.models import training_samples as ts

TWO_PLACES = decimal.Decimal('0.01')

class Learner:
    """ Class responsible for training models, finding the best fit and making
        rate predictions based on the best fit model.
    """

    def __init__(self, instrument, predictor):
        """ Initialize the Learner class based on a predictor and instrument.

            Args:
                instrument: Instrument object.
                predictor: Predictor object.
        """
        self.instrument = instrument
        self.predictor = predictor
        self.init_learning_model()

    def init_learning_model(self):
        """ Initialize the learning model according to the given predictor.

            Args:
                None.
        """
        if self.predictor.name == 'treeRegressor':
            self.model = DecisionTreeRegressor()
            self.best_params = {}

    def generate_all_param_combos(self):
        """ Turn a range of each paramters into a list of all combinations.

            Args:
                None.

            Returns:
                List of Dictionaries. Each entry is a combination of parameters
                    from the paramter range. e.g.
                    [{'max_depth': 4, 'min_samples_split': 5}, ...]
        """
        param_names = []
        param_values = []
        for param_name in self.predictor.parameter_range:
            param_names.append(param_name)
            param_values.append(self.predictor.parameter_range.get(param_name))

        all_param_combos = itertools.product(*param_values)
        all_params = [dict(zip(param_names, x)) for x in all_param_combos]

        return all_params

    def get_training_samples(self, end_date):
        """ Retrieve all training samples before the end date.

            Args:
                before: Date object. Retrieve training samples before end_date.

            Returns:
                all_samples: List of TrainingSample.
        """
        last_date = None
        if end_date is not None:
            last_date = end_date - datetime.timedelta(1)
        all_samples = ts.get_samples(
            instrument=self.instrument,
            end=last_date,
            order_by='date'
        )
        return all_samples

    def learn(self, **kwargs):
        """ Use the training samples for the given instrument to build a
            learning model for the learner.

            Args:
                Named arguments.
                    cv_fold: Integer. Number of folds for cross validation.
                    before: Date object. Use samples before this date.

            Returns:
                None.
        """
        cv_fold = kwargs.get('cv_fold')
        end_date = kwargs.get('before')

        all_training_samples = self.get_training_samples(end_date)
        features = [x.features for x in all_training_samples]
        targets = [x.target for x in all_training_samples]
        best_score = float('-inf')
        best_params = {}
        for params in self.generate_all_param_combos():
            self.model.set_params(**params)
            scores = cross_val_score(self.model, features, targets, cv=cv_fold)
            ave_score = sum(scores) / len(scores)
            if ave_score > best_score:
                best_score = ave_score
                best_params = params

        self.model.set_params(**best_params)
        self.model.fit(features, targets)

    def predict(self, features):
        """ Use trained model to predict profitable change given the features.

            Args:
                features: List of floats.

            Returns:
                Decimal. Predicted profitable change.
        """
        features = np.asarray(features).reshape(1, -1)
        predicted = self.model.predict(features)
        return decimal.Decimal(float(predicted)).quantize(TWO_PLACES)
