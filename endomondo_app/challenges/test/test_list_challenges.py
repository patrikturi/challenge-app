from datetime import date, datetime
from unittest.mock import patch

from challenges.test.helpers import DatabaseTestCase
from challenges.models import Challenge


def _get_by_id(challenges, pk):
    for ch in challenges:
        if ch['id'] == pk:
            return ch
    return None


class ListChallengesTestCase(DatabaseTestCase):

    def setUp(self):
        super().setUp()
        ch4 = Challenge(title='Challenge 4', external_id=12, start_date=date(2020, 6, 1), end_date=date(2020, 6, 30))
        ch5 = Challenge(title='Challenge 5', external_id=13, start_date=date(2018, 1, 1), end_date=date(2018, 1, 30))
        ch6 = Challenge(title='Challenge 6', external_id=14)
        ch4.save()
        ch5.save()
        ch6.save()

        datetime_patch = patch('challenges.views.timezone')
        self.timezone_mock = datetime_patch.start()
        self.timezone_mock.now.return_value = datetime(2020, 2, 25)
        datetime2_patch = patch('challenges.models.challenge.timezone')
        self.timezone2_mock = datetime2_patch.start()
        self.timezone2_mock.now.return_value = datetime(2020, 2, 25)

    def test_all_challenges(self):
        response = self.client.get('/challenges/')

        self.assertEqual(200, response.status_code)
        ids = [ch['id'] for ch in response.data['challenges']]
        self.assertEqual({1, 2, 3, 4, 5, 6, 7}, set(ids))

    def test_challenge_short_view(self):
        response = self.client.get('/challenges/')
        actual_ch = _get_by_id(response.data['challenges'], 1)
        expected_ch = {'id':1, 'title': 'Challenge 0', 'start_date': '2019-11-20'}
        self.assertEqual(expected_ch, dict(actual_ch))

    def test_ended_challenges(self):
        response = self.client.get('/challenges/ended/')

        self.assertEqual(200, response.status_code)
        ids = [ch['id'] for ch in response.data['challenges']]
        self.assertEqual({1, 4, 6}, set(ids))

    def test_upcoming_challenges(self):
        response = self.client.get('/challenges/upcoming/')

        self.assertEqual(200, response.status_code)
        ids = [ch['id'] for ch in response.data['challenges']]
        self.assertEqual({5, 7}, set(ids))

    def test_non_final_challenges(self):
        ch = Challenge(title='Challenge Recently Ended', external_id=30, start_date=date(2020, 2, 1), end_date=date(2020, 2, 25))
        ch.save()

        challenges = Challenge.objects.get_non_final()

        eids = set(ch.external_id for ch in challenges)
        # 5, 6: ongoing
        # 12: upcoming
        # 14: no date
        # 30: recendly ended
        self.assertEqual({5, 6, 12, 14, 30}, eids)
