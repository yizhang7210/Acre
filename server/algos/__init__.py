""" This is the algos package.
    This package is responsible for all price prediction algorithms.
"""

from enum import Enum


class Algos(Enum):
    """ Granularity Enum class. Currently only support DAILY.
    """
    EULER = 'euler'
