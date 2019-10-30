import unittest

from server import database
from server.models import Competitor
from server.competitor_repository import CompetitorRepository


class CompetitorRepositoryTests(unittest.TestCase):

    def setUp(self):
        self.competitor1_id = 123
        self.competitor1 = Competitor(name='Competitor1', endomondo_id=self.competitor1_id, calories=1000)
        self.competitor2 = Competitor(name='Competitor2', endomondo_id=250, calories=1010)
        self.competitors = [self.competitor1, self.competitor2]

        database.init_db()
        self.session = database.session()
        self.repository = CompetitorRepository(self.session)

    def tearDown(self):
        database.drop_tables()

    def test_saveOrUpdate_competitorCreated(self):

        self.repository.save_or_update(self.competitor1)

        competitor = self.session.query(Competitor).filter_by(endomondo_id=self.competitor1_id).one()
        self.assertEqual(self.competitor1.name, competitor.name)
        self.assertEqual(self.competitor1.endomondo_id, competitor.endomondo_id)
        self.assertEqual(self.competitor1.calories, competitor.calories)

    def test_saveOrUpdate_existingCompetitorUpdated(self):
        competitor = Competitor(endomondo_id=self.competitor1_id)
        self.session.add(competitor)
        self.session.commit()

        self.repository.save_or_update(self.competitor1)

        self.session.refresh(competitor)
        self.assertEqual(self.competitor1.name, competitor.name)
        self.assertEqual(self.competitor1.endomondo_id, competitor.endomondo_id)
        self.assertEqual(self.competitor1.calories, competitor.calories)

    def test_saveOrUpdate_existingDisplayNamePreserved(self):
        # Name is parsed from Endomondo but DisplayName can be set in this webapp to override it
        # so DisplayName always will be None when parsing data from Endomondo
        display_name = 'Display Name'
        orig_competitor = Competitor(name='Competitor1', display_name=display_name, endomondo_id=self.competitor1_id, calories=900)
        self.session.add(orig_competitor)
        self.session.commit()

        self.assertEqual(self.competitor1.display_name, None)
        self.repository.save_or_update(self.competitor1)

        competitor = self.session.query(Competitor).filter_by(endomondo_id=self.competitor1_id).one()
        self.assertEqual(display_name, competitor.display_name)
        self.assertEqual(self.competitor1.calories, competitor.calories)

    def test_saveOrUpdateAll_allCompetitorsCreated(self):
        self.repository.save_or_update_all(self.competitors)

        competitors = self.session.query(Competitor).all()
        self.assertEqual(len(self.competitors), len(competitors))