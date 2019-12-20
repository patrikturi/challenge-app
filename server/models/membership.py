from sqlalchemy import Column, Integer, String, ForeignKey

from server.models.abstractbase import AbstractBase


class Membership(AbstractBase):
    __tablename__ = 'memberships'

    id = Column(Integer, primary_key=True)
    competitor_id = Column(Integer, ForeignKey('competitors.id'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
