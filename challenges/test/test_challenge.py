from datetime import date
from unittest.mock import Mock

from django.test import TestCase

from challenges.models import Challenge, Competitor, Stats, ExternalProfile, DataProviderType


class ChallengeTests(TestCase):

    def setUp(self):
        super().setUp()
        self.challenge = Challenge.objects.create(external_id=10, kind=DataProviderType.ENDOMONDO)

        challenge_page = Mock()
        self.challenge_page = challenge_page
        self.challenge_title = 'My Challenge!'
        self.start_date = date(2019, 10, 20)
        self.end_date = date(2020, 1, 22)
        challenge_page.title = self.challenge_title
        challenge_page.end_date = self.end_date
        challenge_page.start_date = self.start_date
        challenge_page.competitors = []

    def test_update_challenge_details(self):
        challenge = self.challenge

        challenge.update(self.challenge_page)

        challenge = Challenge.objects.get(external_id=10)
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

        comp1 = Competitor.objects.create(display_name=orig_display_name)
        profile1 = ExternalProfile.objects.create(competitor=comp1, external_id=comp1_eid, name='Name1', kind=DataProviderType.ENDOMONDO)
        comp2 = Competitor.objects.create()
        profile2 = ExternalProfile.objects.create(competitor=comp2, external_id=comp2_eid, kind=DataProviderType.ENDOMONDO)

        stats1 = Stats.objects.create(challenge=challenge, competitor=comp1, value=2)

        page_comp1 = {'name': 'New Name', 'external_id': comp1_eid, 'calories': 100}
        page_comp2 = {'name': 'Comp2', 'external_id': comp2_eid, 'calories': 111}
        challenge_page.competitors.extend([page_comp1, page_comp2])
        # WHEN
        challenge.update(challenge_page)
        # THEN
        comp1.refresh_from_db()
        profile1.refresh_from_db()
        profile2 = ExternalProfile.objects.get(external_id=comp2_eid)
        stats1.refresh_from_db()
        stats2 = Stats.objects.get(challenge=challenge, competitor=comp2)

        self.assertEqual(page_comp1['name'], profile1.name)
        self.assertEqual(orig_display_name, comp1.display_name)
        self.assertEqual(page_comp1['calories'], stats1.value)
        self.assertEqual(page_comp2['name'], profile2.name)
        self.assertEqual(page_comp2['calories'], stats2.value)
