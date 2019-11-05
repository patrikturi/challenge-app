from sqlalchemy import Column, Integer, ForeignKey

from server.models.abstractbase import AbstractBase


class Calories(AbstractBase):
    __tablename__ = 'calories'
    id = Column(Integer, primary_key=True)
    competitor_id = Column(Integer, ForeignKey('competitors.id'), nullable=False)
    challenge_id = Column(Integer, ForeignKey('challenges.id'), nullable=False)
    kcal = Column(Integer, nullable=False)
