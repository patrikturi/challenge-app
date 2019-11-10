from server.models.competitor import Competitor
from tests.unittests.dbtest_base import DbTestBase


class CompetitorTests(DbTestBase):

    def test_save_competitorStoredToDatabase(self):
        endomondo_id = 200
        name = 'Test Name'
        new_competitor = Competitor(endomondo_id=endomondo_id, name=name)

        queried_competitor = self.session.query(Competitor).filter_by(endomondo_id=endomondo_id).one_or_none()
        self.assertEqual(None, queried_competitor)
        new_competitor.save()

        competitor = self.session.query(Competitor).filter_by(endomondo_id=endomondo_id).one()
        self.assertEqual(name, competitor.name)
        self.assertEqual(endomondo_id, competitor.endomondo_id)

    def test_save_existingCompetitorUpdated(self):
        new_name = 'New Name'
        updated_competitor = Competitor(endomondo_id=self.competitor1.endomondo_id, name=new_name)

        updated_competitor.save()

        self.session.refresh(self.competitor1)
        self.assertEqual(new_name, self.competitor1.name)

    def test_save_existingDisplayNamePreserved(self):
        # Name is parsed from Endomondo but DisplayName can be set in this webapp to override it
        # so DisplayName always will be None when parsing data from Endomondo
        orig_display_name = self.competitor1.display_name
        updated_competitor = Competitor(endomondo_id=self.competitor1.endomondo_id, name=self.competitor1.name)

        self.session.commit()

        self.assertNotEqual(None, orig_display_name)
        self.assertEqual(None, updated_competitor.display_name)
        self.competitor1.save()

        self.session.refresh(self.competitor1)
        self.assertEqual(orig_display_name, self.competitor1.display_name)
