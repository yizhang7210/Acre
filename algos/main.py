""" This is algos.main module.
    This module is the entry point for all algorithms.
"""
from celery import shared_task


@shared_task
def main():
    """ Entry point."""
    print('main')
    # datasource.rates.main()
    # Kick off individual algos
