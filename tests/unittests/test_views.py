from tests.unittests.webtest_base import WebTestBase


class ViewTests(WebTestBase):

    def test_challenges_activeChallengesReturned(self):
        response = self.app.get('/challenges')
        self.assertEqual(response.status_code, 200)
        json = response.get_json()
        self.assertEqual(self.challenge_started1.name, json['data'][0]['name'])
        self.assertEqual(self.challenge_started2.name, json['data'][1]['name'])

    def test_challengesActiveTrue_activeChallengesReturned(self):
        response = self.app.get('/challenges', query_string={'active': True})
        self.assertEqual(response.status_code, 200)
        json = response.get_json()
        self.assertEqual(self.challenge_started1.name, json['data'][0]['name'])
        self.assertEqual(self.challenge_started2.name, json['data'][1]['name'])

    def test_challengesActiveFalse_inactiveChallengesReturned(self):
        response = self.app.get('/challenges', query_string={'active': False})
        self.assertEqual(response.status_code, 200)
        json = response.get_json()
        self.assertEqual(self.challenge_ended1.name, json['data'][0]['name'])
