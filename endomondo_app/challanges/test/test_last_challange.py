from datetime import datetime
from unittest.mock import patch

from challanges.test.helpers import DatabaseTestCase
from challanges.models.challange import Challange


class LastChallangeTests(DatabaseTestCase):

    def setUp(self):
        super().setUp()
        datetime_patch = patch('challanges.views.datetime')
        self.datetime_mock = datetime_patch.start()
        # Both Challange 2 and 3 are ongoing
        self.datetime_mock.now.return_value = datetime(2020, 2, 25)

    def test_ok(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_last_challange(self):
        response = self.client.get('/')
        challange = response.context_data
        self.assertEqual(3, challange['id'])

    def test_all_ended(self):
        self.datetime_mock.now.return_value = datetime(2020, 10, 1)
        response = self.client.get('/')
        challange = response.context_data
        self.assertEqual(2, challange['id'])

    def test_all_ended_one_upcoming(self):
        ch4 = Challange(title='Challange 4', endomondo_id=12, start_date=datetime(2021, 1, 1), end_date=datetime(2021, 1, 30))
        ch4.save()
        self.datetime_mock.now.return_value = datetime(2020, 10, 1)

        response = self.client.get('/')

        challange = response.context_data
        self.assertEqual(2, challange['id'])

    def test_null_start_date(self):
        ch4 = Challange(title='Challange 4', endomondo_id=12)
        ch4.save()

        response = self.client.get('/')

        challange = response.context_data
        self.assertEqual(3, challange['id'])

    def test_all_ended_one_null(self):
        ch4 = Challange(title='Challange 4', endomondo_id=12)
        ch4.save()
        self.datetime_mock.now.return_value = datetime(2020, 10, 1)

        response = self.client.get('/')

        challange = response.context_data
        self.assertEqual(5, challange['id'])
