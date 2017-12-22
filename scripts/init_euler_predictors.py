# pylint: disable=missing-docstring
from algos.euler.models import predictors


def initialize_euler_predictors():
    param_range = {
        'max_depth': [4, 5, 6],
        'min_samples_split': [1000, 2000, 3000, 4000, 5000]
    }
    predictors.insert_many([
        predictors.create_one(
            name='treeRegressor', parameter_range=param_range
        )
    ])

# To implement RunScript interface.
def run():
    initialize_euler_predictors()
