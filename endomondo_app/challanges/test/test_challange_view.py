from challanges.test.helpers import DatabaseTestCase


class ChallangeViewTests(DatabaseTestCase):

    def test_ok(self):
        response = self.client.get('/challange/2/')

        self.assertEqual(200, response.status_code)

    def test_challange_view(self):
        response = self.client.get('/challange/2/')

        expected_challange = {
            'id': 2,
            'endomondo_id': 5,
            'title': 'Challange 1',
            'start_date': self.ch1_start,
            'end_date': self.ch1_end
        }

        challange = response.context_data
        del challange['teams']
        self.assertEqual(expected_challange, challange)

    def test_team_view(self):
        response = self.client.get('/challange/2/')

        team = response.context_data['teams'][0]
        del team['members']

        expected_team = {
            'id': 1,
            'name': 'Team A',
            'challange': 2,
            'calories': 1501,
        }
        
        self.assertEqual(expected_team, team)

    def test_team_members(self):
        expected_members = [
            {
                'id': 1,
                'endomondo_id': 10,
                'name': 'Competitor 1',
                'display_name': '',
                'calories': 1001
            },
            {
                'id': 3,
                'endomondo_id': 25,
                'name': 'Competitor 3',
                'display_name': 'Competitor C',
                'calories': 500
            },
            {
                'id': 4,
                'endomondo_id': 26,
                'name': 'Competitor 4',
                'display_name': ''
            }
        ]

        response = self.client.get('/challange/2/')

        team = response.context_data['teams'][0]
        members = team['members']
        self.assertEqual(expected_members, members)

    def test_challange_parts(self):

        response = self.client.get('/challange/2/')

        challange = response.context_data
        self.assertEqual('Challange 1', challange['title'])
        teams = [team['name'] for team in challange['teams']]
        self.assertEqual(['Team A', 'Team B'], teams)
