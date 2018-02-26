# pylint: disable=missing-docstring
from algos.euler.models import predictors

TREE_PARAMS = {
    'max_depth': [4, 5, 6],
    'min_samples_split': [1000, 2000, 3000, 4000, 5000]
}

SVM_PARAMS = {
    'max_iter': [500]
}


def initialize_euler_predictors():
    predictors.insert_many([
        predictors.create_one(
            name='treeRegressor', parameter_range=TREE_PARAMS
        ),
        predictors.create_one(
            name='linearSVMRegressor', parameter_range=SVM_PARAMS
        ),
    ])


# To implement RunScript interface.
def run():
    initialize_euler_predictors()
