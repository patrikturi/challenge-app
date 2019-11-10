import os
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import Mock

from server.background_service import BackgroundService


class TestBackgroundService(unittest.TestCase):

    def test_fetchActiveChallenges_updateChallengeCalled(self):
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        page1_raw = Path(current_file_path, 'resources/challenge_page1.html').read_text(encoding='utf-8')
        query_util = Mock()
        endomondo_api = Mock()
        current_date = date(2018, 1, 1)

        challenge1 = Mock()
        challenge2 = Mock()
        challenge1.endomondo_id = 5
        challenge2.endomondo_id = 6
        query_util.get_active_challenges.return_value = [challenge1, challenge2]

        endomondo_api.get_page.return_value = page1_raw

        service = BackgroundService(endomondo_api, query_util)
        service.fetch_active_challenges(current_date)

        challenge1.update.assert_called_once()
        challenge2.update.assert_called_once()
