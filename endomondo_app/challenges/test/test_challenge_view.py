from django.http import HttpResponseNotFound

from challenges.test.helpers import DatabaseTestCase


class ChallengeViewTests(DatabaseTestCase):

    def test_ok(self):
        response = self.client.get('/challenge/2/')
        self.assertEqual(200, response.status_code)

    def test_challenge_view(self):
        response = self.client.get('/challenge/2/')

        expected_challenge = {
            'id': 2,
            'endomondo_id': '5',
            'title': 'Challenge 1',
            'start_date': self.ch1_start,
            'end_date': self.ch1_end,
            'parse_date': None,
            'parse_error': None,
            'status_text': '-',
        }

        challenge = response.context_data['challenge']
        del challenge['teams']
        self.assertEqual(expected_challenge, challenge)

    def test_team_view(self):
        response = self.client.get('/challenge/2/')

        team = response.context_data['challenge']['teams'][0]
        del team['members']

        expected_team = {
            'id': 1,
            'name': 'Team A',
            'challenge': 2,
            'calories': 1501,
        }

        self.assertEqual(expected_team, team)

    def test_team_members(self):
        expected_members = [
            {
                'id': 1,
                'endomondo_id': '10',
                'name': 'Competitor 1',
                'calories': 1001
            },
            {
                'id': 3,
                'endomondo_id': '25',
                'name': 'Competitor C', # should contain dispaly_name if both name and display_name are provided
                'calories': 500
            },
            {
                'id': 4,
                'endomondo_id': '26',
                'name': 'Competitor 4',
                'calories': 0
            }
        ]

        response = self.client.get('/challenge/2/')

        team = response.context_data['challenge']['teams'][0]
        members = team['members']
        self.assertEqual(expected_members, members)

    def test_challenge_parts(self):

        response = self.client.get('/challenge/2/')

        challenge = response.context_data['challenge']
        self.assertEqual('Challenge 1', challenge['title'])
        teams = [team['name'] for team in challenge['teams']]
        self.assertEqual(['Team A', 'Team B'], teams)

    def test_challenge_does_not_exist(self):
        response = self.client.get('/challenge/1000/')
        self.assertTrue(isinstance(response, HttpResponseNotFound))
