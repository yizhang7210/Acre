""" This is the datasource module.
    This module is responsible for common setups of data sources.
"""
from enum import Enum


class Granularity(Enum):
    """ Granularity Enum class. Currently only support DAILY.
    """
    DAILY = 'D'
