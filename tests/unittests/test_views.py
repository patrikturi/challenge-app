from tests.unittests.webtest_base import WebTestBase


class ChallengeViewTests(WebTestBase):

    def test_challenges_activeChallengesReturned(self):
        response = self.app.get('/challenges')
        data = self.assert_success(response)
        self.assertEqual(self.challenge_started1.name, data[0]['name'])
        self.assertEqual(self.challenge_started2.name, data[1]['name'])

    def test_challengesActiveTrue_activeChallengesReturned(self):
        response = self.app.get('/challenges', query_string={'active': True})
        data = self.assert_success(response)
        self.assertEqual(self.challenge_started1.name, data[0]['name'])
        self.assertEqual(self.challenge_started2.name, data[1]['name'])

    def test_challengesActiveFalse_inactiveChallengesReturned(self):
        response = self.app.get('/challenges', query_string={'active': False})
        data = self.assert_success(response)
        self.assertEqual(self.challenge_ended1.name, data[0]['name'])

    def test_postChallenge_challengeCreated(self):
        endomondo_id = 120
        response = self.app.post('/challenges', json={'endomondo_id': endomondo_id})
        data = self.assert_success(response)
        json = response.get_json()
        self.assertEqual(True, json['success'])
        self.assertEqual(endomondo_id, data['endomondo_id'])

    def test_postChallengeExistingId_errorMessageReturned(self):
        response = self.app.post('/challenges', json={'endomondo_id': self.challenge1_endomondo_id})
        self.assert_failure(response, 'already exists')

    def test_postChallengeNotInteger_errorMessageReturned(self):
        response = self.app.post('/challenges', json={'endomondo_id': 'a' })
        self.assert_failure(response, 'not a number')

    def test_postChallengeNotInteger_errorMessageReturned(self):
        response = self.app.post('/challenges', json={})
        self.assert_failure(response, 'not provided')
