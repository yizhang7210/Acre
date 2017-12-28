""" This is the datasource package.
    This package is responsible for retrieve historical rates from a data source.
"""
from enum import Enum


class Granularity(Enum):
    """ Granularity Enum class. Currently only support DAILY.
    """
    DAILY = 'D'
