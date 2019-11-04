from server.tests.webtest_base import WebTestBase


class ViewTests(WebTestBase):

    def test_challenges_active_returnsActiveChallenges(self):
        response = self.app.get('/challenges/active')
        self.assertEqual(response.status_code, 200)
        json = response.get_json()
        self.assertEqual(self.challenge_started1.name, json['data'][0]['name'])
        self.assertEqual(self.challenge_started2.name, json['data'][1]['name'])

    def test_challenges_active_returnsInactiveChallenges(self):
        response = self.app.get('/challenges/inactive')
        self.assertEqual(response.status_code, 200)
        json = response.get_json()
        self.assertEqual(self.challenge_ended1.name, json['data'][0]['name'])
