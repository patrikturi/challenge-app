from server import errors
from server.models.calories import Calories
from server.models.membership import Membership
from server.models.team import Team


class RepositoryUtil:

    def __init__(self, session):
        self.session = session

    def save_all(self, model_objects):
        for model in model_objects:
            model.save()

    def save_calories(self, challenge_id, page):
        for competitor in page.competitors:
            kcal = page.get_calories(competitor.id)
            calories = Calories(challenge_id=challenge_id, competitor_id=competitor.id, kcal=kcal)
            calories.save()
        self.session.commit()

    def insert_challenge(self, endomondo_id):
        # Avoids circular import
        from server.models.challenge import Challenge

        challenge_same_id = self.session.query(Challenge).filter_by(endomondo_id=endomondo_id).one_or_none()
        if challenge_same_id:
            raise errors.UserError(f'Challenge with endomondo id {endomondo_id} already exists.')

        new_challenge = Challenge(endomondo_id=endomondo_id)
        self.session.add(new_challenge)
        self.session.commit()
        return new_challenge

    def insert_team(self, name, challenge_id):
        team_same_id = self.session.query(Team).filter_by(name=name).one_or_none()

        if team_same_id:
            raise errors.UserError(f'Team with name {name} already exists.')

        new_team = Team(name=name, challenge_id=challenge_id)
        self.session.add(new_team)
        self.session.commit()
        return new_team

    def remove_team(self, team_id):
        self.session.query(Membership).filter_by(team_id=team_id).delete()
        self.session.query(Team).filter_by(id=team_id).delete()
        self.session.commit()

    def insert_team_member(self, team_id, competitor_id):
        team = self.session.query(Team).filter_by(id=team_id).one()

        cnt = self.session.query(Membership, Team).filter_by(competitor_id=competitor_id).join(Team).filter(Team.challenge_id == team.challenge_id).count()
        if cnt:
            raise errors.UserError('Competitor already has a team in this Challenge')

        new_membership = Membership(team_id=team_id, competitor_id=competitor_id)
        self.session.add(new_membership)
        self.session.commit()

        return new_membership

    def remove_team_member(self, team_id, competitor_id):
        membership = self.session.query(Membership).filter_by(competitor_id=competitor_id, team_id=team_id).one()
        self.session.delete(membership)
        self.session.commit()

    def get_team_members(self, team_id):
        return self.session.query(Membership).filter_by(team_id=team_id).all()
