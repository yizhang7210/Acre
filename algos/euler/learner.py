""" This is algos.euler.learner module.
    This module is responsible for training the models and make predictions.
"""
import itertools

from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor

from algos.euler.models import training_samples as ts


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

    def learn(self):
        """ Use the training samples for the given instrument to build a
            learning model for the learner.

            Args:
                None.

            Returns:
                None.
        """
        all_data = ts.get_samples(instrument=self.instrument, order_by='date')
        features = [x.features for x in all_data]
        targets = [x.target for x in all_data]
        best_score = 0
        best_params = {}
        for params in self.generate_all_param_combos():
            self.model.set_params(**params)
            scores = cross_val_score(self.model, features, targets, cv=10)
            ave_score = sum(scores) / len(scores)
            if ave_score > best_score:
                best_score = ave_score
                best_params = params

        self.model.set_params(**best_params)
        self.model.fit(features, targets)

# Main
# for ins in instruments.get_all():
#     for pred in predictors.get_all():
#         learner = Learner(ins, pred)
#         learner.learn()
#         learner.predict()
