from server.models import Challenge


class ChallengeRepository:

    def __init__(self, session, competitor_repository):
        self.session = session
        self.competitor_repository = competitor_repository

    def get_all_active(self, current_date):
        pass

    def update(self, endomondo_id, challenge_page):
        challenge = self.session.query(Challenge).filter_by(endomondo_id=endomondo_id).one()

        challenge.name = challenge_page.title
        challenge.start_date = challenge_page.start_date
        challenge.end_date = challenge_page.end_date
        self.session.commit()

        self.competitor_repository.save_or_update_all(challenge_page.competitors)
