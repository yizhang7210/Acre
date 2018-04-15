# pylint: disable=missing-docstring
import datetime
import json

from algos.euler.models import training_samples as ts
from algos.euler.models import predictions, predictors
from core.models import instruments
from rest_framework.test import APITestCase


class EulerAPITest(APITestCase):

    @classmethod
    def setUpClass(cls):
        super(EulerAPITest, cls).setUpClass()
        cls.set_up_instruments()
        cls.set_up_training_samples()
        cls.set_up_predictors()
        cls.set_up_predictions()

    @classmethod
    def set_up_instruments(cls):
        cls.eur_usd = instruments.Instrument(name='EUR_USD', multiplier=10000)
        cls.eur_usd.save()

        cls.usd_jpy = instruments.Instrument(name='USD_JPY', multiplier=100)
        cls.usd_jpy.save()

    @classmethod
    def set_up_training_samples(cls):
        day_one = datetime.date(2017, 12, 15)
        sample_one = ts.create_one(
            instrument=cls.eur_usd, date=day_one,
            target=3.4, features=[])

        day_two = datetime.date(2017, 12, 18)
        sample_two = ts.create_one(
            instrument=cls.usd_jpy, date=day_two,
            target=-8.9, features=[])
        sample_three = ts.create_one(
            instrument=cls.eur_usd, date=day_two,
            target=13.6, features=[])

        ts.insert_many([sample_one, sample_two, sample_three])

    @classmethod
    def set_up_predictors(cls):
        cls.predictor = predictors.create_one(
            name="test-predictor", parameters={})
        cls.predictor.save()

    @classmethod
    def set_up_predictions(cls):
        day_one = datetime.date(2017, 12, 12)
        pred_one = predictions.create_one(
            instrument=cls.eur_usd, date=day_one, profitable_change=100,
            score=0.4, predictor=cls.predictor)

        day_two = datetime.date(2017, 12, 17)
        pred_two = predictions.create_one(
            instrument=cls.usd_jpy, date=day_two, profitable_change=150,
            score=0.3, predictor=cls.predictor)
        pred_three = predictions.create_one(
            instrument=cls.eur_usd, date=day_two, profitable_change=-180,
            score=0.2, predictor=cls.predictor)

        predictions.insert_many([pred_one, pred_two, pred_three])

    @classmethod
    def tearDownClass(cls):
        super(EulerAPITest, cls).tearDownClass()
        predictions.delete_all()
        ts.delete_all()
        instruments.delete_all()

    def test_profitable_changes(self):
        # When
        url = '/v1/algos/euler/profitable_changes'
        response = self.client.get(url)

        # Then
        self.assertEqual(len(json.loads(response.content.decode('utf-8'))), 3)

        # When
        url = '/v1/algos/euler/profitable_changes?instrument=USD_JPY'
        response = self.client.get(url)

        # Then
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0].get('instrument'), 'USD_JPY')
        self.assertEqual(content[0].get('profitable_change'), -8.9)

        # When
        url = '/v1/algos/euler/profitable_changes?start=2017-12-18'
        response = self.client.get(url)

        # Then
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(content), 2)

        # When
        url = '/v1/algos/euler/profitable_changes?end=2017-12-15'
        response = self.client.get(url)

        # Then
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0].get('instrument'), 'EUR_USD')

        # When
        url = '/v1/algos/euler/profitable_changes?order_by=-date,instrument'
        response = self.client.get(url)

        # Then
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(content), 3)
        self.assertEqual(content[0].get('instrument'), 'EUR_USD')
        self.assertEqual(content[0].get('date'), '2017-12-18')
        self.assertEqual(content[0].get('profitable_change'), 13.6)
        self.assertEqual(content[1].get('instrument'), 'USD_JPY')
        self.assertEqual(content[1].get('date'), '2017-12-18')
        self.assertEqual(content[1].get('profitable_change'), -8.9)
        self.assertEqual(content[2].get('instrument'), 'EUR_USD')
        self.assertEqual(content[2].get('date'), '2017-12-15')
        self.assertEqual(content[2].get('profitable_change'), 3.4)

    def test_predicted_changes(self):
        # When
        url = '/v1/algos/euler/predicted_changes'
        response = self.client.get(url)

        # Then
        self.assertEqual(len(json.loads(response.content.decode('utf-8'))), 3)

        # When
        url = '/v1/algos/euler/predicted_changes?instrument=USD_JPY'
        response = self.client.get(url)

        # Then
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0].get('instrument'), 'USD_JPY')
        self.assertEqual(content[0].get('predicted_change'), 150)

        # When
        url = '/v1/algos/euler/predicted_changes?start=2017-12-17'
        response = self.client.get(url)

        # Then
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(content), 2)

        # When
        url = '/v1/algos/euler/predicted_changes?end=2017-12-12'
        response = self.client.get(url)

        # Then
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0].get('instrument'), 'EUR_USD')

        # When
        url = '/v1/algos/euler/predicted_changes?order_by=-date,instrument'
        response = self.client.get(url)

        # Then
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(content), 3)
        self.assertEqual(content[0].get('instrument'), 'EUR_USD')
        self.assertEqual(content[0].get('date'), '2017-12-17')
        self.assertEqual(content[0].get('predicted_change'), -180)
        self.assertEqual(content[1].get('instrument'), 'USD_JPY')
        self.assertEqual(content[1].get('date'), '2017-12-17')
        self.assertEqual(content[1].get('predicted_change'), 150)
        self.assertEqual(content[2].get('instrument'), 'EUR_USD')
        self.assertEqual(content[2].get('date'), '2017-12-12')
        self.assertEqual(content[2].get('predicted_change'), 100)
