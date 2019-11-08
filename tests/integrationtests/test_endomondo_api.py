import os
import unittest

from server.endomondo_api import EndomondoApi


class EndomondoApiTests(unittest.TestCase):

    def test_getPage_fetchesChallengePage(self):
        username = 'mentor.endomondo@gmail.com'
        url = 'https://www.endomondo.com/challenges/41375412'
        password = os.environ['ENDOMONDO_USER_PASSWORD']

        api = EndomondoApi()
        api.login(username, password)
        body = api.get_page(url)
        motto = 'Fun, Health, Friendship, BeachBody, Sport, Teambuilding'
        self.assertTrue(motto in body)
