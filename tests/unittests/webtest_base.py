import unittest
from datetime import date

from server import create_app
from server.database import init_db, drop_tables, session
from server.models.challenge import Challenge


class WebTestBase(unittest.TestCase):

    def setUp(self):
        config = {
            'TESTING': True,
            'DATABASE': 'sqlite://',
            'MOCK_DATE': date(2019, 2, 5)
        }
        app = create_app(config)

        self.app = app.test_client()
        init_db()
        self.session = session()

        # Add some test data
        self.challenge1_endomondo_id = 5
        self.challenge_started1 = Challenge(name='Challenge Running1', endomondo_id=self.challenge1_endomondo_id, start_date=date(2019, 2, 1), end_date=date(2019, 2, 10))
        self.challenge_started2 = Challenge(name='Challenge Running2', endomondo_id=6, start_date=date(2019, 2, 2), end_date=date(2019, 2, 11))
        self.challenge_ended1 = Challenge(name='Challenge Ended1', endomondo_id=7, start_date=date(2019, 1, 1), end_date=date(2019, 1, 30))
        self.session.add(self.challenge_started1)
        self.session.add(self.challenge_started2)
        self.session.add(self.challenge_ended1)
        self.session.commit()

        self.context = app.test_request_context()
        self.context.push()

    def tearDown(self):
        self.context.pop()
        drop_tables()
        self.session.close()

    def assert_success(self, response):
        self.assertEqual(response.status_code, 200)
        resp_json = response.get_json()
        self.assertEqual(True, resp_json['success'])
        return resp_json.get('data')

    def assert_failure(self, response, expected_message):
        self.assertEqual(response.status_code, 200)
        resp_json = response.get_json()
        self.assertEqual(False, resp_json['success'])
        if expected_message:
            self.assertTrue(expected_message in resp_json['message'])
        return resp_json.get('message')
