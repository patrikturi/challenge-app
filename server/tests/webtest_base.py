from server import create_app
from server.database import init_db, drop_tables

import unittest


class WebTestBase(unittest.TestCase):

    def setUp(self):
        config = {'TESTING': True, 'DATABASE': 'sqlite://'}
        app = create_app(config)

        self.app = app.test_client()
        init_db()
        self.context = app.test_request_context()
        self.context.push()

    def tearDown(self):
        self.context.pop()
        drop_tables()
