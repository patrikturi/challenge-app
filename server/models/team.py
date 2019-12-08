from sqlalchemy import Column, Integer, String, ForeignKey

from server.models.abstractbase import AbstractBase


class Team(AbstractBase):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    challenge_id = Column(Integer, ForeignKey('challenges.id'), nullable=False)
