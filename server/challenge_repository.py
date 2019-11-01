from sqlalchemy import or_, and_

from server.models import Challenge


class ChallengeRepository:

    def __init__(self, session, competitor_repository):
        self.db_session = session
        self.competitor_repository = competitor_repository

    def get_all_active(self, current_date):
        return self.db_session.query(Challenge).filter(
            or_(Challenge.start_date == None, Challenge.end_date == None,
                and_(Challenge.start_date <= current_date, Challenge.end_date >= current_date))).all()

    def get_all_inactive(self, current_date):
        return self.db_session.query(Challenge).filter(or_(
            Challenge.start_date > current_date, Challenge.end_date < current_date)).all()

    def update(self, endomondo_id, challenge_page):
        challenge = self.db_session.query(Challenge).filter_by(endomondo_id=endomondo_id).one()

        challenge.name = challenge_page.title
        challenge.start_date = challenge_page.start_date
        challenge.end_date = challenge_page.end_date
        self.db_session.commit()

        self.competitor_repository.save_or_update_all(challenge_page.competitors)
