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

        self.current_date = date(2019, 2, 15)
        self.challenge_ended = Challenge(endomondo_id=1, start_date=date(2019, 2, 5), end_date=date(2019, 2, 14))
        self.challenge_running1 = Challenge(endomondo_id=2, start_date=date(2019, 2, 15), end_date=date(2019, 2, 28))
        self.challenge_running2 = Challenge(endomondo_id=3, start_date=date(2019, 2, 10), end_date=date(2019, 2, 20))
        self.challenge_not_started = Challenge(endomondo_id=4, start_date=date(2019, 2, 16), end_date=date(2019, 2, 22))
        # NOTE:
        # * having neither start_date and end_date happens when the challenge wasn't ever fetched/parsed yet
        # * having only start date or end date is not a use case for this application
        self.challenge_without_date = Challenge(endomondo_id=5)
        self.session.add(self.challenge_ended)
        self.session.add(self.challenge_running1)
        self.session.add(self.challenge_running2)
        self.session.add(self.challenge_without_date)
        self.session.add(self.challenge_not_started)
        self.session.commit()

    def tearDown(self):
        database.drop_tables()

    def test_update_challengeUpdated(self):
        challenge = self.challenge_without_date
        remote_id = challenge.endomondo_id

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

    def test_getAllActive_returnsChallengesRunningOrWithoutDate(self):

        all_active = self.repository.get_all_active(self.current_date)

        self.assertEqual(3, len(all_active))
        self.assertEqual(self.challenge_running1.endomondo_id, all_active[0].endomondo_id)
        self.assertEqual(self.challenge_running2.endomondo_id, all_active[1].endomondo_id)
        self.assertEqual(self.challenge_without_date.endomondo_id, all_active[2].endomondo_id)

    def test_getAllInactive_returnsChallengesStoppedOrNotStarted(self):

        all_inactive = self.repository.get_all_inactive(self.current_date)

        self.assertEqual(2, len(all_inactive))
        self.assertEqual(self.challenge_ended.endomondo_id, all_inactive[0].endomondo_id)
        self.assertEqual(self.challenge_not_started.endomondo_id, all_inactive[1].endomondo_id)
