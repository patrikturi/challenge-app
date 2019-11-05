from server.models.calories import Calories


class CaloriesRepository:

    def __init__(self, db_session):
        self.db_session = db_session

    def save_calories(self, challenge_id, page):
        for competitor in page.competitors:
            kcal = page.get_calories(competitor.endomondo_id)
            calories = self.db_session.query(Calories).filter_by(challenge_id=challenge_id, competitor_id=competitor.endomondo_id).one_or_none()
            if calories:
                calories.kcal = kcal
            else:
                calories = Calories(challenge_id=challenge_id, competitor_id=competitor.endomondo_id, kcal=kcal)
                self.db_session.add(calories)
        self.db_session.commit()

    def get_challenge_calories(self, challenge_id):
        all_calories = self.db_session.query(Calories).filter_by(challenge_id=challenge_id).all()
        return {calories.competitor_id: calories.kcal for calories in all_calories}
