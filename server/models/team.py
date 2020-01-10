from sqlalchemy import Column, Integer, String, ForeignKey

from server.models.abstractbase import AbstractBase
from server.models.competitor import Competitor
from server.models.membership import Membership


class Team(AbstractBase):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    challenge_id = Column(Integer, ForeignKey('challenges.id'), nullable=False)

    def as_view(self):
        memberships, competitors = self.session.query(Membership).filter_by(team_id=self.id).join(Competitor, Membership.competitor_id == Competitor.id).all()
        comp_views = [comp.as_dict() for comp in competitors]
        self_dict = self.asdict()
        self_dict['members'] = comp_views
        return self_dict
