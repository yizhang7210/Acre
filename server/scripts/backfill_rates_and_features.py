# pylint: disable=missing-docstring

from algos.euler import transformer as euler_tsfr
from datasource import rates


# To implement RunScript interface.
def run():
    rates.run()
    euler_tsfr.run()
