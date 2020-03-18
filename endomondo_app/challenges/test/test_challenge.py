from datetime import datetime
from django.test import TestCase
from unittest.mock import Mock

from challenges.models.challenge import Challenge
from challenges.models.competitor import Competitor
from challenges.models.stats import Stats


class ChallengeTests(TestCase):

    def setUp(self):
        super().setUp()
        challenge = Challenge(endomondo_id=10)
        self.challenge = challenge
        challenge.save()
 
        challenge_page = Mock()
        self.challenge_page = challenge_page
        self.challenge_title = 'My Endomondo Challenge!'
        self.start_date = datetime(2019, 10, 20)
        self.end_date = datetime(2020, 1, 22)
        challenge_page.title = self.challenge_title
        challenge_page.end_date = self.end_date
        challenge_page.start_date = self.start_date
        challenge_page.competitors = []

    def test_update_challenge_details(self):
        challenge = self.challenge

        challenge.update(self.challenge_page)

        challenge = Challenge.objects.get(endomondo_id=10)
        self.assertEqual(self.challenge_title, challenge.title)
        self.assertEqual(self.start_date, challenge.start_date)
        self.assertEqual(self.end_date, challenge.end_date)

    def test_update_competitors(self):
        # IF
        challenge = self.challenge
        challenge_page = self.challenge_page
        orig_display_name = 'Display Name'
        comp1_eid = 5
        comp2_eid = 20

        comp1_orig = Competitor(endomondo_id=comp1_eid, name='Name1', display_name=orig_display_name)
        comp1_orig.save()

        stats1_orig = Stats(challenge=challenge, competitor=comp1_orig, calories=2)
        stats1_orig.save()

        page_comp1 = {'name': 'New Name', 'endomondo_id': comp1_eid, 'calories': 100}
        page_comp2 = {'name': 'Comp2', 'endomondo_id': comp2_eid, 'calories': 111}
        challenge_page.competitors.extend([page_comp1, page_comp2])
        # WHEN
        challenge.update(self.challenge_page)
        # THEN
        comp1 = Competitor.objects.get(endomondo_id=comp1_eid)
        comp2 = Competitor.objects.get(endomondo_id=comp2_eid)
        stats1 = Stats.objects.get(challenge=challenge, competitor=comp1)
        stats2 = Stats.objects.get(challenge=challenge, competitor=comp2)

        self.assertEqual(page_comp1['name'], comp1.name)
        self.assertEqual(orig_display_name, comp1.display_name)
        self.assertEqual(page_comp1['calories'], stats1.calories)
        self.assertEqual(page_comp2['name'], comp2.name)
        self.assertEqual(page_comp2['calories'], stats2.calories)
