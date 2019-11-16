from server.models.calories import Calories
from tests.unittests.dbtest_base import DbTestBase


class TestCalories(DbTestBase):

    def test_save_caloriesStoredToDatabase(self):
        kcal = 200
        challenge_id = self.challenge1.id
        competitor_id = self.competitor1.id
        new_calories = Calories(challenge_id=challenge_id, competitor_id=competitor_id, kcal=kcal)

        calories_queried = self.session.query(Calories).filter_by(challenge_id=challenge_id,
                                                                  competitor_id=competitor_id).one_or_none()
        self.assertEqual(None, calories_queried)
        new_calories.save()
        self.session.commit()

        calories = self.session.query(Calories).filter_by(challenge_id=challenge_id,
                                                          competitor_id=competitor_id).one()
        self.assertEqual(kcal, calories.kcal)

    def test_save_existingCaloriesUpdated(self):

        challenge_id = self.challenge1.id
        competitor_id = self.competitor1.id
        calories = Calories(challenge_id=challenge_id, competitor_id=competitor_id, kcal=200)
        self.session.add(calories)
        self.session.commit()

        new_kcal = 300
        calories.kcal = new_kcal
        calories.save()
        self.session.commit()

        self.session.refresh(calories)
        self.assertEqual(new_kcal, calories.kcal)
