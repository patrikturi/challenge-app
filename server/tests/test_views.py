from flask import url_for

from server.tests.webtest_base import WebTestBase


class ChallengeViewTests(WebTestBase):

    def test_challenges_active_returnsActiveChallenges(self):
        response = self.app.get('/challenges/active')
        self.assertEqual(response.status_code, 200)
        json = response.get_json()
        self.assertEqual(json['data'][0]['name'], 'Challenge1')
        self.assertEqual(json['data'][1]['name'], 'Challenge2')
