from datetime import date, datetime
from unittest.mock import patch

from challenges.test.helpers import DatabaseTestCase
from challenges.models.challenge import Challenge


class LastChallengeTests(DatabaseTestCase):

    def setUp(self):
        super().setUp()
        datetime_patch = patch('challenges.views.timezone')
        self.timezone_mock = datetime_patch.start()
        # Both Challenge 2 and 3 are ongoing
        self.timezone_mock.now.return_value = datetime(2020, 2, 25)

    def test_ok(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_last_challenge(self):
        response = self.client.get('/')
        challenge = response.context_data['challenge']
        self.assertEqual(3, challenge['id'])

    def test_all_ended(self):
        self.timezone_mock.now.return_value = datetime(2020, 10, 1)
        response = self.client.get('/')
        challenge = response.context_data['challenge']
        self.assertEqual(2, challenge['id'])

    def test_all_ended_one_upcoming(self):
        ch4 = Challenge(title='Challenge 4', endomondo_id=12, start_date=date(2021, 1, 1), end_date=date(2021, 1, 30))
        ch4.save()
        self.timezone_mock.now.return_value = datetime(2020, 10, 1)

        response = self.client.get('/')

        challenge = response.context_data['challenge']
        self.assertEqual(2, challenge['id'])

    def test_null_start_date(self):
        ch4 = Challenge(title='Challenge 4', endomondo_id=12)
        ch4.save()

        response = self.client.get('/')

        challenge = response.context_data['challenge']
        self.assertEqual(3, challenge['id'])

    def test_all_ended_one_null(self):
        ch4 = Challenge(title='Challenge 4', endomondo_id=12)
        ch4.save()
        self.timezone_mock.now.return_value = datetime(2020, 10, 1)

        response = self.client.get('/')

        challenge = response.context_data['challenge']
        self.assertEqual(5, challenge['id'])
