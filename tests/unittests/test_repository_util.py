from unittest.mock import Mock

from server.models.calories import Calories
from server.utils.repository_util import RepositoryUtil
from tests.unittests.dbtest_base import DbTestBase


class RepositoryUtilTests(DbTestBase):

    def setUp(self):
        super().setUp()

        self.competitor1_kcal = 100
        self.id_to_calories = {self.competitor1.id: self.competitor1_kcal, self.competitor2.id: 150}
        self.page = Mock()
        self.page.competitors = [self.competitor1]
        self.page.get_calories.side_effect = lambda id: self.id_to_calories[id]

        self.repo_util = RepositoryUtil(self.session)

    def test_saveAll_allCompetitorsCreated(self):
        comp1 = Mock()
        comp2 = Mock()
        competitors = [comp1, comp2]
        self.repo_util.save_all(competitors)

        comp1.save.assert_called_once()
        comp2.save.assert_called_once()

    def test_saveCalories_caloriesStoredToDatabase(self):
        self.repo_util.save_calories(self.challenge.id, self.page)

        comp1_calories = self.session.query(Calories).filter_by(competitor_id=self.competitor1.id, challenge_id=self.challenge.id).one()
        self.assertEqual(self.id_to_calories[self.competitor1.id], comp1_calories.kcal)

    def test_saveCalories_caloriesKcalUpdated(self):
        self.store_calories(self.competitor1, 5)

        self.repo_util.save_calories(self.challenge.id, self.page)

        comp1_calories = self.session.query(Calories).filter_by(competitor_id=self.competitor1.id, challenge_id=self.challenge.id).one()
        self.assertEqual(self.competitor1_kcal, comp1_calories.kcal)
