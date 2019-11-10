from datetime import date
from unittest.mock import Mock

from tests.unittests.dbtest_base import DbTestBase


class ChallengeTests(DbTestBase):

    def test_update_challengeUpdated(self):
        challenge = self.challenge_without_date
        challenge.repo_util = Mock()

        challenge_page = Mock()
        name = 'My Endomondo Challenge!'
        start_date = date(2019, 10, 20)
        end_date = date(2020, 1, 22)
        challenge_page.title = name
        challenge_page.start_date = start_date
        challenge_page.end_date = end_date

        challenge_page.competitors = Mock()

        challenge.update(challenge_page)

        self.session.refresh(challenge)
        self.assertEqual(name, challenge.name)
        self.assertEqual(start_date, challenge.start_date)
        self.assertEqual(end_date, challenge.end_date)

        challenge.repo_util.save_all.assert_called_once_with(challenge_page.competitors)
        challenge.repo_util.save_calories.assert_called_once_with(challenge.id, challenge_page)

    def test_getChallengeCalories_mapWithCompetitorEndomondoIdToCaloriesReturned(self):
        competitor1_kcal = 100
        self.store_calories(self.competitor1, competitor1_kcal)

        calories = self.challenge.get_calories()

        self.assertEqual(competitor1_kcal, calories[self.competitor1.id])
