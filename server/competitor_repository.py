from sqlalchemy import or_, and_

from server.challenge_page import ChallengePage
from server.models import Challenge, Competitor


class CompetitorRepository:
    """Fetch and save challenge data to the database"""

    def __init__(self, session):
        self.session = session

    def save_or_update_all(self, competitors):
        for comp in competitors:
            self.save_or_update(comp)

    def save_or_update(self, competitor):
        stored_competitor = self.session.query(Competitor).filter_by(endomondo_id=competitor.endomondo_id).first()

        if stored_competitor:
            competitor.id = stored_competitor.id
            self.session.merge(competitor)
        else:
            self.session.add(competitor)

        self.session.commit()
