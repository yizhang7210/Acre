# pylint: disable=missing-docstring
from algos.euler.models import predictors


def initialize_euler_predictors():
    param_range = {
        'max_depth': list(range(4, 11, 2)),
        'min_samples_split': list(range(10, 50, 8))
    }
    predictors.insert_many([
        predictors.create_one(
            name='treeRegressor', parameter_range=param_range
        )
    ])

# To implement RunScript interface.
def run():
    initialize_euler_predictors()
