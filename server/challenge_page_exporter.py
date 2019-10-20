from server.models import Challenge, Competitor


class ChallengePageExporter:
    """Save challenge data to the database"""

    def save_challenge(self, session, endomondo_id, challenge_page):
        challenge = session.query(Challenge).filter_by(endomondo_id=endomondo_id).one()

        challenge.name = challenge_page.title
        challenge.start_date = challenge_page.start_date
        challenge.end_date = challenge_page.end_date
        session.commit()

    def save_users(self, session, users):
        for user in users:
            self._save_user(session, user)

    def _save_user(self, session, user):
        # FIXME: use named tuple
        name = user[0]
        endomondo_id = user[1]
        calories = user[2]
        competitor = session.query(Competitor).filter_by(endomondo_id=endomondo_id).first()
        competitor_exists = bool(competitor)
        if not competitor_exists:
            competitor = Competitor(endomondo_id=endomondo_id)
        # TODO: skip database commit if no change
        competitor.name = name
        competitor.calories = calories
        if not competitor_exists:
            session.add(competitor)
        session.commit()
