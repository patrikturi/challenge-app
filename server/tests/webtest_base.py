from datetime import date
import unittest

from server import create_app
from server.database import init_db, drop_tables, session
from server.models import Challenge


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

        # Add some test data
        started_ch1 = Challenge(name='Challenge1', endomondo_id=5, start_date=date(2019, 2, 1), end_date=date(2019, 2, 10))
        started_ch2 = Challenge(name='Challenge2', endomondo_id=6, start_date=date(2019, 2, 2), end_date=date(2019, 2, 11))
        ended_ch = Challenge(name='Challenge3', endomondo_id=7, start_date=date(2019, 1, 1), end_date=date(2019, 1, 30))
        session.add(started_ch1)
        session.add(started_ch2)
        session.add(ended_ch)
        session.commit()

        self.context = app.test_request_context()
        self.context.push()

    def tearDown(self):
        self.context.pop()
        drop_tables()
