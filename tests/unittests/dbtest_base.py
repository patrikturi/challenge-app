import unittest
from datetime import date

from server import database
from server.models.calories import Calories
from server.models.challenge import Challenge
from server.models.competitor import Competitor
from server.models.membership import Membership
from server.models.team import Team


class DbTestBase(unittest.TestCase):

    def setUp(self):
        database.init_db()
        self.session = database.session()

        self.current_date = date(2019, 2, 15)
        self.challenge_ended = Challenge(endomondo_id=11, start_date=date(2019, 2, 5), end_date=date(2019, 2, 14))
        self.session.add(self.challenge_ended)
        self.challenge_running1 = Challenge(endomondo_id=12, start_date=date(2019, 2, 15), end_date=date(2019, 2, 28))
        self.session.add(self.challenge_running1)
        self.challenge_running2 = Challenge(endomondo_id=13, start_date=date(2019, 2, 10), end_date=date(2019, 2, 20))
        self.session.add(self.challenge_running2)
        self.challenge_not_started = Challenge(endomondo_id=14, start_date=date(2019, 2, 16), end_date=date(2019, 2, 22))
        self.session.add(self.challenge_not_started)
        self.challenge_without_date = Challenge(endomondo_id=15)
        self.session.add(self.challenge_without_date)

        self.challenge1_endomondo_id = 111112
        self.challenge1 = Challenge(name='Challenge1', endomondo_id=self.challenge1_endomondo_id)
        self.session.add(self.challenge1)

        self.competitor1_id = 123
        self.competitor1 = Competitor(name='Competitor1', endomondo_id=self.competitor1_id, display_name='Display Name')
        self.session.add(self.competitor1)
        self.competitor2 = Competitor(name='Competitor2', endomondo_id=250)
        self.session.add(self.competitor2)
        self.competitors = [self.competitor1, self.competitor2]

        self.team1 = Team(name='Team1', challenge_id=self.challenge_ended.endomondo_id)
        self.session.add(self.team1)
        self.team2 = Team(name='Team2', challenge_id=self.challenge_ended.endomondo_id)
        self.session.add(self.team2)
        # Team in another competition
        self.team1b = Team(name='Team1b', challenge_id=self.challenge_not_started.endomondo_id)
        self.session.add(self.team1b)

        self.session.commit()

        # competitor2_membership = Membership(team_id=self.team1.id, competitor_id=self.competitor2.id)
        # self.session.add(competitor2_membership)
        # self.session.commit()

    def tearDown(self):
        database.drop_tables()
        self.session.close()

    def store_calories(self, competitor, kcal):
        calories = Calories(challenge_id=self.challenge1.id, competitor_id=competitor.id, kcal=kcal)
        self.session.add(calories)
        self.session.commit()
