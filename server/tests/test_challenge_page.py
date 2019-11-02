import unittest
from pathlib import Path
import os
from datetime import date

from server.challenge_page import ChallengePage
from server.models import Competitor


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
        self.assertEqual('/?x=-next-page-url', self.page1.next_page_url)

    def test_page1_hasNoPrevPage(self):
        self.assertEqual(None, self.page1.prev_page_url)

    def test_page2_hasNoNextPage(self):
        self.assertEqual(None, self.page2.next_page_url)

    def test_page2_hasPrevPage(self):
        self.assertEqual('/?x=-prev-page-url', self.page2.prev_page_url)

    def test_page1_title(self):
        self.assertEqual('Challenge Title! - 2019', self.page1.title)

    def test_page1_competitors(self):
        expected_competitors = [
            Competitor(name='Competitor1', endomondo_id=903),
            Competitor(name='Árvíztűrő tükörfúrógép', endomondo_id=926),
            Competitor(name='Competitor3', endomondo_id=8)
        ]
        self.assert_competitors(expected_competitors, self.page1.competitors)
        self.assert_calories(self.page1, {903: 25702, 926: 22564, 8: 16360})

    def test_page2_user5HasNoWorkouts(self):
        expected_competitors = [
            Competitor(name='Competitor4', endomondo_id=299),
            Competitor(name='Competitor5 No workouts', endomondo_id=661)
        ]
        self.assert_competitors(expected_competitors, self.page2.competitors)
        self.assert_calories(self.page2, {299: 2978, 661: 0})

    def test_notStartedPage_competitorsHaveZeroKcal(self):
        expected_competitors = [
            Competitor(name='Competitor1', endomondo_id=190),
            Competitor(name='Competitor2', endomondo_id=115)
        ]
        self.assert_competitors(expected_competitors, self.not_started_page.competitors)
        self.assert_calories(self.not_started_page, {190: 0, 115: 0})

    def test_invalidCaloriesPage_raisesException(self):
        self.assertRaises(ValueError, lambda: self.invalid_calories_page.competitors)

    def test_page1_startDate(self):
        self.assertEqual(date(2019, 10, 1), self.page1.start_date)

    def test_page1_endDate(self):
        self.assertEqual(date(2019, 10, 31), self.page1.end_date)

    def assert_competitors(self, expected_list, actual_list):
        for expected, actual in zip(expected_list, actual_list):
            if expected.name != actual.name or expected.endomondo_id != actual.endomondo_id:
                exp_str = self._competitor_assert_str(expected)
                act_str = self._competitor_assert_str(actual)
                raise AssertionError(f'Competitors not equal. Expected: {exp_str} Actual: {act_str}')

    def assert_calories(self, page, expected_calories):
        for competitor in page.competitors:
            endomondo_id = competitor.endomondo_id
            self.assertEqual(expected_calories[endomondo_id], page.get_calories(endomondo_id))

    def _competitor_assert_str(self, expected):
        return f'(name={expected.name}, endomondo_id={expected.endomondo_id})'
