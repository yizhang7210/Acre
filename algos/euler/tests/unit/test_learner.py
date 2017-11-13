# pylint: disable=missing-docstring
from unittest import TestCase

from algos.euler.learner import Learner
from algos.euler.models import predictors


class LearnerTest(TestCase):

    def test_expand_params(self):
        # Given
        param_range = {
            'max_depth': range(4, 11, 2),
            'min_samples_split': range(2, 21, 4),
        }
        pred = predictors.create_one(parameter_range=param_range)

        # When
        l = Learner(None, pred)
        all_params = l.generate_all_param_combos()

        # Then
        self.assertEqual(len(all_params), 20)
        self.assertEqual(all_params[0].get('min_samples_split'), 2)
        self.assertEqual(all_params[5].get('max_depth'), 6)
