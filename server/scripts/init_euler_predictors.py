# pylint: disable=missing-docstring
from algos.euler.models import predictors

TREE_PARAMS = {
    'max_depth': 5,
    'min_samples_split': 2000
}

SVM_PARAMS = {
    'max_iter': 500
}


def initialize_euler_predictors():
    predictors.insert_many([
        predictors.create_one(
            name='treeRegressor', parameters=TREE_PARAMS
        ),
        predictors.create_one(
            name='linearSVMRegressor', parameters=SVM_PARAMS
        ),
    ])


# To implement RunScript interface.
def run():
    initialize_euler_predictors()
