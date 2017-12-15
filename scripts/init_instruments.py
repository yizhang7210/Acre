# pylint: disable=missing-docstring
from datasource.models import instruments


def initialize_instruments():
    instruments.insert_many([
        instruments.create_one(name='EUR_USD', multiplier=10000),
        instruments.create_one(name='GBP_USD', multiplier=10000),
        instruments.create_one(name='USD_CAD', multiplier=10000),
        instruments.create_one(name='USD_CHF', multiplier=10000),
        instruments.create_one(name='USD_JPY', multiplier=100),
    ])

# To implement RunScript interface.
def run():
    initialize_instruments()
