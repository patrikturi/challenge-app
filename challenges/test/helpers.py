from datetime import date

from django.test import TestCase

from challenges.models import Challenge, Competitor, Team, Stats, ExternalProfile, DataProviderType, ChallengeTypes


class DatabaseTestCase(TestCase):
    def setUp(self):
        self.ch1_start = date(2020, 2, 1)
        self.ch1_end = date(2020, 3, 15)
        ch0 = Challenge.objects.create(title='Challenge 0', external_id=4, start_date=date(2019, 11, 20), end_date=date(2019, 11, 25), kind=ChallengeTypes.STRAVA)
        ch1 = Challenge.objects.create(title='Challenge 1', external_id=5, start_date=self.ch1_start, end_date=self.ch1_end, kind=ChallengeTypes.STRAVA)
        ch2 = Challenge.objects.create(title='Challenge 2', external_id=6, start_date=date(2020, 2, 10), end_date=date(2020, 2, 29), kind=ChallengeTypes.STRAVA)
        ch3 = Challenge.objects.create(title='Challenge 3', external_id=2, start_date=date(2019, 6, 1), end_date=date(2019, 6, 30), kind=ChallengeTypes.STRAVA)
        t1 = Team.objects.create(name='Team A', challenge=ch1)
        t2 = Team.objects.create(name='Team B', challenge=ch1)
        t3 = Team.objects.create(name='Team C', challenge=ch2)
        comp1 = Competitor.objects.create()
        comp2 = Competitor.objects.create()
        comp3 = Competitor.objects.create(display_name='Competitor C')
        comp4 = Competitor.objects.create()
        comp5 = Competitor.objects.create()
        comp6 = Competitor.objects.create()
        comp7 = Competitor.objects.create()
        ExternalProfile.objects.create(competitor=comp1, external_id=10, name='Competitor 1', kind=DataProviderType.STRAVA)
        ExternalProfile.objects.create(competitor=comp2, external_id=20, name='Competitor 2', kind=DataProviderType.STRAVA)
        ExternalProfile.objects.create(competitor=comp3, external_id=25, name='Competitor 3', kind=DataProviderType.STRAVA)
        ExternalProfile.objects.create(competitor=comp4, external_id=26, name='Competitor 4', kind=DataProviderType.STRAVA)
        ExternalProfile.objects.create(competitor=comp5, external_id=27, name='Competitor 5', kind=DataProviderType.STRAVA)
        ExternalProfile.objects.create(competitor=comp6, external_id=28, name='Competitor 6', kind=DataProviderType.STRAVA)
        ExternalProfile.objects.create(competitor=comp7, external_id=29, name='Competitor 7', kind=DataProviderType.STRAVA)
        comp1.teams.add(t1)
        comp3.teams.add(t1)
        comp4.teams.add(t1)
        comp5.teams.add(t3)
        comp6.teams.add(t2)
        comp7.teams.add(t2)
        comp1.save()
        comp3.save()
        comp4.save()
        comp5.save()
        comp6.save()
        comp7.save()

        comp1_stats = Stats.objects.create(value=1001, competitor=comp1, challenge=ch1)
        comp2_stats = Stats.objects.create(value=500, competitor=comp3, challenge=ch1)
        comp5_stats = Stats.objects.create(value=2000, competitor=comp5, challenge=ch2)
        comp6_stats = Stats.objects.create(value=100, competitor=comp6, challenge=ch1)
        comp7_stats = Stats.objects.create(value=20, competitor=comp7, challenge=ch1)
