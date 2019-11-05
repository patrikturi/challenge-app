from server.models.competitor import Competitor


class CompetitorRepository:
    """Fetch and save challenge data to the database"""

    def __init__(self, session):
        self.db_session = session

    def save_or_update_all(self, competitors):
        for comp in competitors:
            self.save_or_update(comp)

    def save_or_update(self, competitor):
        stored_competitor = self.db_session.query(Competitor).filter_by(endomondo_id=competitor.endomondo_id).first()

        if stored_competitor:
            competitor.id = stored_competitor.id
            self.db_session.merge(competitor)
        else:
            self.db_session.add(competitor)

        self.db_session.commit()
