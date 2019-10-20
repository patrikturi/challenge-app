import unittest
from unittest.mock import Mock
from datetime import date

from server import database
from server.challenge_page_exporter import ChallengePageExporter
from server.models import Challenge
from server.models import Competitor


class ChallengePageExporterTests(unittest.TestCase):

    def setUp(self):
        database.init_db()
        self.session = database.session()

        self.user1_id = 123
        self.user2_id = 250
        self.user1 = ('User1', self.user1_id, 1000)
        self.user2 = ('User2', self.user2_id, 1010)
        self.users = [self.user1, self.user2]

    def tearDown(self):
        database.drop_tables()

    def test_saveChallenge_challengeUpdated(self):
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

        exporter = ChallengePageExporter()
        exporter.save_challenge(self.session, remote_id, challenge_page)

        self.session.refresh(challenge)
        self.assertEqual(name, challenge.name)
        self.assertEqual(start_date, challenge.start_date)
        self.assertEqual(end_date, challenge.end_date)

    def test_saveUsersNotExisting_newUsersCreated(self):
        exporter = ChallengePageExporter()
        exporter.save_users(self.session, self.users)

        competitor1 = self.session.query(Competitor).filter_by(endomondo_id=self.user1_id).one()
        competitor2 = self.session.query(Competitor).filter_by(endomondo_id=self.user2_id).one()

        user1_saved = (competitor1.name, competitor1.endomondo_id, competitor1.calories)
        user2_saved = (competitor2.name, competitor2.endomondo_id, competitor2.calories)
        self.assertEqual(self.user1, user1_saved)
        self.assertEqual(self.user2, user2_saved)

    def test_saveUsersExisting_usersUpdated(self):
        comp1 = Competitor(name='UserA', endomondo_id=self.user1_id, calories=11)
        comp2 = Competitor(name='UserB', endomondo_id=self.user2_id, calories=12)
        self.session.add(comp1)
        self.session.add(comp2)
        self.session.commit()

        exporter = ChallengePageExporter()
        exporter.save_users(self.session, self.users)

        competitor1 = self.session.query(Competitor).filter_by(endomondo_id=self.user1_id).one()
        competitor2 = self.session.query(Competitor).filter_by(endomondo_id=self.user2_id).one()

        user1_saved = (competitor1.name, competitor1.endomondo_id, competitor1.calories)
        user2_saved = (competitor2.name, competitor2.endomondo_id, competitor2.calories)
        self.assertEqual(self.user1, user1_saved)
        self.assertEqual(self.user2, user2_saved)
