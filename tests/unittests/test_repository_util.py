from unittest.mock import Mock

from server import errors
from server.errors import UserError
from server.models.calories import Calories
from server.models.challenge import Challenge
from server.models.membership import Membership
from server.models.team import Team
from server.utils.repository_util import RepositoryUtil
from tests.unittests.dbtest_base import DbTestBase


class RepositoryUtilTests(DbTestBase):

    def setUp(self):
        super().setUp()

        self.competitor1_kcal = 100
        self.id_to_calories = {self.competitor1.id: self.competitor1_kcal, self.competitor2.id: 150}
        self.page = Mock()
        self.page.competitors = [self.competitor1]
        self.page.get_calories.side_effect = lambda id: self.id_to_calories[id]

        self.repo_util = RepositoryUtil(self.session)

    def test_saveAll_allCompetitorsCreated(self):
        comp1 = Mock()
        comp2 = Mock()
        competitors = [comp1, comp2]
        self.repo_util.save_all(competitors)

        comp1.save.assert_called_once()
        comp2.save.assert_called_once()

    def test_saveCalories_caloriesStoredToDatabase(self):
        self.repo_util.save_calories(self.challenge1.id, self.page)

        comp1_calories = self.session.query(Calories).filter_by(competitor_id=self.competitor1.id, challenge_id=self.challenge1.id).one()
        self.assertEqual(self.id_to_calories[self.competitor1.id], comp1_calories.kcal)

    def test_saveCalories_caloriesKcalUpdated(self):
        self.store_calories(self.competitor1, 5)

        self.repo_util.save_calories(self.challenge1.id, self.page)

        comp1_calories = self.session.query(Calories).filter_by(competitor_id=self.competitor1.id, challenge_id=self.challenge1.id).one()
        self.assertEqual(self.competitor1_kcal, comp1_calories.kcal)

    def test_insertChallenge_challengeStoredToDatabase(self):
        endomondo_id = 1000
        self.repo_util.insert_challenge(endomondo_id)

        self.session.query(Challenge).filter_by(endomondo_id=endomondo_id).one()

    def test_insertChallengeIdAlreadyExists_userErrorRaised(self):
        self.assertRaises(errors.UserError, lambda: self.repo_util.insert_challenge(self.challenge1_endomondo_id))

    def test_insertTeam_teamStoredToDatabase(self):
        name = 'New Team'
        self.repo_util.insert_team(name, self.challenge1.id)

        self.session.query(Team).filter_by(name=name).one()

    def test_insertTeamIdAlreadyExists_userErrorRaised(self):
        self.assertRaises(errors.UserError, lambda: self.repo_util.insert_team('Team1', self.challenge1.id))


    def test_insertTeamMember_teamMemberStoredToDatabase(self):

        self.repo_util.insert_team_member(self.team1.id, self.competitor1.id)

        self.session.query(Membership).filter_by(competitor_id=self.competitor1.id).one()

    def test_insertTeamMember_competitorAlreadyInCompetition_raisesError(self):
        new_membership = Membership(team_id=self.team2.id, competitor_id=self.competitor1.id)
        self.session.add(new_membership)
        self.session.commit()
        self.session.query(Membership).filter_by(competitor_id=self.competitor1.id).one()

        self.assertRaises(UserError, lambda: self.repo_util.insert_team_member(self.team1.id, self.competitor1.id))

    def test_insertTeamMember_competitorInAnotherCompetition_teamMemberStoredToDatabase(self):
        new_membership = Membership(team_id=self.team1b.id, competitor_id=self.competitor1.id)
        self.session.add(new_membership)
        self.session.commit()
        self.session.query(Membership).filter_by(competitor_id=self.competitor1.id).one()

        self.repo_util.insert_team_member(self.team1.id, self.competitor1.id)
        self.session.query(Membership).filter_by(competitor_id=self.competitor1.id).join(Team).filter(Team.challenge_id == self.team1.challenge_id).one()
