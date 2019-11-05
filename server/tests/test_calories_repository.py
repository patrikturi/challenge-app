import unittest
from unittest.mock import Mock

from server import database
from server.calories_repository import CaloriesRepository
from server.models.competitor import Competitor
from server.models.challenge import Challenge
from server.models.calories import Calories


class CaloriesRepositoryTests(unittest.TestCase):

    def setUp(self):
        self.challenge_id = 11112
        self.challenge = Challenge(name='Challenge1', endomondo_id=self.challenge_id)

        self.competitor1_id = 123
        self.competitor2_id = 250
        self.competitor1 = Competitor(name='Competitor1', endomondo_id=self.competitor1_id)
        self.competitor2 = Competitor(name='Competitor2', endomondo_id=self.competitor2_id)
        self.competitors = [self.competitor1, self.competitor2]
        self.competitor1_kcal = 100
        self.id_to_calories = {self.competitor1_id: self.competitor1_kcal, self.competitor2_id: 150}

        database.init_db()
        self.session = database.session()
        self.session.add(self.challenge)
        self.session.add(self.competitor1)
        self.session.add(self.competitor2)
        self.session.commit()

        self.repository = CaloriesRepository(self.session)
        self.page = Mock()
        self.page.competitors = [self.competitor1]
        self.page.get_calories.side_effect = lambda id: self.id_to_calories[id]

    def tearDown(self):
        database.drop_tables()

    def test_saveCalories_storesCaloriesRecord(self):
        self.repository.save_calories(self.challenge_id, self.page)

        comp1_calories = self.session.query(Calories).filter_by(competitor_id=self.competitor1_id, challenge_id=self.challenge_id).one()
        self.assertEqual(self.id_to_calories[self.competitor1_id], comp1_calories.kcal)

    def test_saveCalories_caloriesKcalUpdated(self):
        self._store_calories(self.competitor1, 5)

        self.repository.save_calories(self.challenge_id, self.page)

        comp1_calories = self.session.query(Calories).filter_by(competitor_id=self.competitor1_id, challenge_id=self.challenge_id).one()
        self.assertEqual(self.competitor1_kcal, comp1_calories.kcal)

    def test_getChallengeCalories_returnsMapWithCompetitorEndomondoIdToCalories(self):
        self._store_calories(self.competitor1, self.competitor1_kcal)

        calories = self.repository.get_challenge_calories(self.challenge_id)

        self.assertEqual(self.competitor1_kcal, calories[self.competitor1_id])

    def _store_calories(self, competitor, kcal):
        calories = Calories(challenge_id=self.challenge_id, competitor_id=competitor.endomondo_id, kcal=kcal)
        self.session.add(calories)
        self.session.commit()
