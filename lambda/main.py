import requests

DEV_URL = 'http://api-dev.acre.one'


def lambda_handler(event, context):
    if event['event'] == 'daily-update':
        suffix = '/v1/algos/update/end_of_day'
    elif event['event'] == 'daily-clean':
        suffix = '/v1/algos/update/clean'

    requests.post(DEV_URL + suffix)
