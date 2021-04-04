import os
import unittest
from datetime import date
from pathlib import Path

from challenges.endomondo.challenge_page import ChallengePage


class ChallengePageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        page1_raw = Path(current_file_path, 'resources/challenge_page1.html').read_text(encoding='utf-8')
        page2_raw = Path(current_file_path, 'resources/challenge_page2.html').read_text(encoding='utf-8')
        not_started_raw = Path(current_file_path, 'resources/challenge_not_started.html').read_text(encoding='utf-8')
        invalid_calories_raw = Path(current_file_path, 'resources/challenge_invalid_calories.html').read_text(encoding='utf-8')
        cls.page1 = ChallengePage(page1_raw)
        cls.page2 = ChallengePage(page2_raw)
        cls.not_started_page = ChallengePage(not_started_raw)
        cls.invalid_calories_page = ChallengePage(invalid_calories_raw)

    def test_page1_hasNextPage(self):
        self.assertEqual('https://endomondo.com/?x=-next-page-url', self.page1.next_page_url)

    def test_page1_hasNoPrevPage(self):
        self.assertEqual(None, self.page1.prev_page_url)

    def test_page2_hasNoNextPage(self):
        self.assertEqual(None, self.page2.next_page_url)

    def test_page2_hasPrevPage(self):
        self.assertEqual('https://endomondo.com/?x=-prev-page-url', self.page2.prev_page_url)

    def test_page1_title(self):
        self.assertEqual('Challenge Title! - 2019', self.page1.title)

    def test_page1_competitors(self):
        expected_competitors = [
            {'name': 'Competitor1', 'external_id': 903, 'calories': 25702},
            {'name': 'Árvíztűrő tükörfúrógép', 'external_id': 926, 'calories': 22564},
            {'name': 'Competitor3', 'external_id': 8, 'calories': 16360},
        ]
        self.assertEqual(expected_competitors, self.page1.competitors)

    def test_page2_user5HasNoWorkouts(self):
        expected_competitors = [
            {'name': 'Competitor4', 'external_id': 299, 'calories': 2978},
            {'name': 'Competitor5 No workouts', 'external_id': 661, 'calories': 0},
        ]
        self.assertEqual(expected_competitors, self.page2.competitors)

    def test_notStartedPage_competitorsHaveZeroKcal(self):
        expected_competitors = [
            {'name': 'Competitor1', 'external_id': 190, 'calories': 0},
            {'name': 'Competitor2', 'external_id': 115, 'calories': 0},
        ]
        self.assertEqual(expected_competitors, self.not_started_page.competitors)

    def test_invalidCaloriesPage_raisesException(self):
        self.assertRaises(ValueError, lambda: self.invalid_calories_page.competitors)

    def test_page1_startDate(self):
        self.assertEqual(date(2019, 10, 1), self.page1.start_date)

    def test_page1_endDate(self):
        self.assertEqual(date(2019, 10, 31), self.page1.end_date)
