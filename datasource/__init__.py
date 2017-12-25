""" This is the datasource module.
    This module is responsible for common setups of data sources.
"""
import json
import os
from enum import Enum

APP_DIR = os.path.dirname(os.path.realpath(__file__))

class Granularity(Enum):
    """ Granularity Enum class. Currently only support DAILY.
    """
    DAILY = 'D'

def get_credentials():
    """ Retrieve credentials for data source integration.
    """
    acre_env = os.environ.get('ACRE_ENV')

    if acre_env is None or acre_env == 'LOCAL':
        creds = json.load(open('{0}/credentials.json'.format(APP_DIR), 'r'))
    else:
        creds = {
            "Token-Trade": os.environ.get('TOKEN_TRADE'),
            "Token-Game": os.environ.get('TOKEN_GAME')
        }

    return creds
