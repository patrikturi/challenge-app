from sqlalchemy import Column, Integer, ForeignKey

from server.models.abstractbase import AbstractBase
from server.models.competitor import Competitor


class Calories(AbstractBase):
    __tablename__ = 'calories'
    id = Column(Integer, primary_key=True)
    competitor_id = Column(Integer, ForeignKey('competitors.id'), nullable=False)
    challenge_id = Column(Integer, ForeignKey('challenges.id'), nullable=False)
    kcal = Column(Integer, nullable=False)

    def save(self):
        calories = self.session.query(Calories).filter_by(challenge_id=self.challenge_id,
                                                          competitor_id=self.competitor_id).one_or_none()
        if calories:
            calories.kcal = self.kcal
        else:
            self.session.add(self)
