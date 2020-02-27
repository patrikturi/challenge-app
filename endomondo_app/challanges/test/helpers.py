from datetime import datetime

from django.test import TestCase

from challanges.models.challange import Challange
from challanges.models.team import Team
from challanges.models.competitor import Competitor
from challanges.models.stats import Stats


class DatabaseTestCase(TestCase):
    def setUp(self):
        self.ch1_start = datetime(2020, 2, 1)
        self.ch1_end = datetime(2020, 3, 1)
        ch0 = Challange(title='Challange 0', endomondo_id=5, start_date=datetime(2019, 11, 20), end_date=datetime(2019, 11, 25))
        ch1 = Challange(title='Challange 1', endomondo_id=5, start_date=self.ch1_start, end_date=self.ch1_end)
        ch2 = Challange(title='Challange 2', endomondo_id=6, start_date=datetime(2020, 1, 15), end_date=datetime(2020, 3, 15))
        ch0.save()
        ch1.save()
        ch2.save()
        t1 = Team(name='Team A', challange=ch1)
        t2 = Team(name='Team B', challange=ch1)
        t3 = Team(name='Team C', challange=ch2)
        t1.save()
        t2.save()
        t3.save()
        comp1 = Competitor(endomondo_id=10, name='Competitor 1')
        comp2 = Competitor(endomondo_id=20, name='Competitor 2')
        comp3 = Competitor(endomondo_id=25, name='Competitor 3', display_name='Competitor C')
        comp4 = Competitor(endomondo_id=26, name='Competitor 4')
        comp5 = Competitor(endomondo_id=27, name='Competitor 5')
        comp1.save()
        comp2.save()
        comp3.save()
        comp4.save()
        comp5.save()
        comp1.teams.add(t1)
        comp3.teams.add(t1)
        comp4.teams.add(t1)
        comp5.teams.add(t3)
        comp1.save()
        comp3.save()
        comp4.save()
        comp5.save()

        comp1_stats = Stats(calories=1001, competitor=comp1, challange=ch1)
        comp2_stats = Stats(calories=500, competitor=comp3, challange=ch1)
        comp5_stats = Stats(calories=2000, competitor=comp5, challange=ch2)
        comp1_stats.save()
        comp2_stats.save()
        comp5_stats.save()

