import unittest
from datetime import date
from unittest.mock import Mock

from server import database
from server.challenge_repository import ChallengeRepository
from server.models import Challenge


class ChallengeRepositoryTests(unittest.TestCase):

    def setUp(self):
        database.init_db()
        self.session = database.session()
        self.competitor_repository = Mock()
        self.repository = ChallengeRepository(self.session, self.competitor_repository)

    def tearDown(self):
        database.drop_tables()

    def test_update_challengeUpdated(self):
        remote_id = 111
        challenge = Challenge(endomondo_id=remote_id)
        self.session.add(challenge)
        self.session.commit()

        challenge_page = Mock()

        name = 'My Endomondo Challenge!'
        start_date = date(2019, 10, 20)
        end_date = date(2020, 1, 22)

        challenge_page.title = name
        challenge_page.start_date = start_date
        challenge_page.end_date = end_date

        challenge_page.competitors = Mock()

        self.repository.update(remote_id, challenge_page)

        self.session.refresh(challenge)
        self.assertEqual(name, challenge.name)
        self.assertEqual(start_date, challenge.start_date)
        self.assertEqual(end_date, challenge.end_date)

        self.competitor_repository.save_or_update_all.assert_called_once_with(challenge_page.competitors)

    def test_getAllActive_returnsChallengeRunning(self):
        current_date = date(2019, 2, 15)
        challenge_ended = Challenge(endomondo_id=1, start_date=date(2019, 2, 5), end_date=date(2019, 2, 14))
        challenge_running = Challenge(endomondo_id=2, start_date=date(2019, 2, 15), end_date=date(2019, 2, 28))
        challenge_not_started = Challenge(endomondo_id=3, start_date=date(2019, 2, 16), end_date=date(2019, 2, 22))
        self.session.add(challenge_ended)
        self.session.add(challenge_running)
        self.session.add(challenge_not_started)
        self.session.commit()

        all_active = self.repository.get_all_active(current_date)

        self.assertEqual(1, len(all_active))
        self.assertEqual(challenge_running.endomondo_id, all_active[0].endomondo_id)
