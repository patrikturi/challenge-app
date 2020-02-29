from datetime import datetime
from unittest.mock import patch

from challanges.test.helpers import DatabaseTestCase
from challanges.models.challange import Challange


def _get_by_id(challanges, id):
    for ch in challanges:
        if ch['id'] == id:
            return ch
    return None


class ListChallangesTestCase(DatabaseTestCase):

    def setUp(self):
        super().setUp()
        ch4 = Challange(title='Challange 4', endomondo_id=12, start_date=datetime(2020, 6, 1), end_date=datetime(2020, 6, 30))
        ch5 = Challange(title='Challange 5', endomondo_id=13, start_date=datetime(2018, 1, 1), end_date=datetime(2018, 1, 30))
        ch6 = Challange(title='Challange 6', endomondo_id=14)
        ch4.save()
        ch5.save()
        ch6.save()

        datetime_patch = patch('challanges.views.datetime')
        self.datetime_mock = datetime_patch.start()
        self.datetime_mock.now.return_value = datetime(2020, 2, 25)

    def test_all_challanges(self):
        response = self.client.get('/challanges/')

        self.assertEqual(200, response.status_code)
        ids = [ch['id'] for ch in response.context_data['challanges']]
        self.assertEqual({1, 2, 3, 4, 5, 6, 7}, set(ids))

    def test_challange_short_view(self):
        response = self.client.get('/challanges/')
        actual_ch = _get_by_id(response.context_data['challanges'], 1)
        expected_ch = {'id': 1, 'title': 'Challange 0', 'start_date': datetime(2019, 11, 20)}
        self.assertEqual(expected_ch, actual_ch)

    def test_ended_challanges(self):
        response = self.client.get('/challanges/ended/')

        self.assertEqual(200, response.status_code)
        ids = [ch['id'] for ch in response.context_data['challanges']]
        self.assertEqual({1, 4, 6}, set(ids))

    def test_upcoming_challanges(self):
        response = self.client.get('/challanges/upcoming/')

        self.assertEqual(200, response.status_code)
        ids = [ch['id'] for ch in response.context_data['challanges']]
        self.assertEqual({5, 7}, set(ids))
