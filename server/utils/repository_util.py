from server.models.calories import Calories


class RepositoryUtil:

    def __init__(self, session):
        self.session = session

    def save_all(self, model_objects):
        for model in model_objects:
            model.save()

    def save_calories(self, challenge_id, page):
        for competitor in page.competitors:
            kcal = page.get_calories(competitor.id)
            calories = Calories(challenge_id=challenge_id, competitor_id=competitor.id, kcal=kcal)
            calories.save()
        self.session.commit()
