import unittest
from pathlib import Path
import os

from server.challenge_page import ChallengePage


class ChallengePageTests(unittest.TestCase):

    def setUp(self):
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        page1_raw = Path(current_file_path, 'resources/challenge_page1.html').read_text(encoding='utf-8')
        page2_raw = Path(current_file_path, 'resources/challenge_page2.html').read_text(encoding='utf-8')
        not_started_raw = Path(current_file_path, 'resources/challenge_not_started.html').read_text(encoding='utf-8')
        invalid_calories_raw = Path(current_file_path, 'resources/challenge_invalid_calories.html').read_text(encoding='utf-8')
        self.page1 = ChallengePage(page1_raw)
        self.page2 = ChallengePage(page2_raw)
        self.not_started_page = ChallengePage(not_started_raw)
        self.invalid_calories_page = ChallengePage(invalid_calories_raw)

    def test_page1_hasNextPage(self):
        self.assertEqual('/?x=-next-page-url', self.page1.next_page_url)

    def test_page1_hasNoPrevPage(self):
        self.assertEqual(None, self.page1.prev_page_url)

    def test_page2_hasNoNextPage(self):
        self.assertEqual(None, self.page2.next_page_url)

    def test_page2_hasPrevPage(self):
        self.assertEqual('/?x=-prev-page-url', self.page2.prev_page_url)

    def test_page1_users(self):
        expected_users = [
            ('Valid User1', '903', 25702),
            ('Valid User árvíztűrő tükörfúrógép', '926', 22564),
            ('Valid User3', '008', 16360)
        ]
        self.assertListEqual(expected_users, self.page1.users)

    def test_notStartedPage_usersHaveZeroKcal(self):
        expected_users = [
            ('Valid User1', '190', 0),
            ('Valid User2', '115', 0)
        ]
        self.assertListEqual(expected_users, self.not_started_page.users)

    def test_invalodCaloriesPage_raisesException(self):
        self.assertRaises(ValueError, lambda: self.invalid_calories_page.users)
