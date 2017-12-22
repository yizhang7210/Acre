# pylint: disable=missing-docstring
from algos.euler.models import predictors


def initialize_euler_predictors():
    param_range = {
        'max_depth': [5, 10, 15, 20],
        'min_samples_split': [50, 100, 200, 500]
    }
    predictors.insert_many([
        predictors.create_one(
            name='treeRegressor', parameter_range=param_range
        )
    ])

# To implement RunScript interface.
def run():
    initialize_euler_predictors()
