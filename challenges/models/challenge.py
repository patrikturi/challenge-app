from datetime import timedelta

from django.db import models
from django.db.models import Q
from django.utils import timezone


class ChallengeManager(models.Manager):

    def get_last(self, now):
        try:
            challenge = self.filter(Q(start_date__lte=now, end_date__gte=now) | Q(start_date__isnull=True)).latest('start_date')
        except self.model.DoesNotExist:
            challenge = self.filter(end_date__lt=now).latest('end_date')

        return challenge

    def get_non_final(self):
        """These are the challenges to be updated periodically from the 3rd party"""
        # Upcoming or Ongoing or Completed just lately
        end = timezone.now() - timedelta(days=1)
        challenges = self.filter(Q(end_date__gt=end) | Q(end_date__isnull=True)).order_by('-start_date')
        return challenges


class Challenge(models.Model):

    external_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200, blank=True)
    start_date = models.DateField('Start date', null=True, blank=True)
    end_date = models.DateField('End date', null=True, blank=True)
    parse_error = models.NullBooleanField()
    status_text = models.CharField(max_length=200, default='-')
    parse_date = models.DateTimeField('Parse date', null=True, blank=True)
    objects = ChallengeManager()

    def update(self, challenge_page):
        from challenges.models import Competitor, Stats

        self.title = challenge_page.title
        self.start_date = challenge_page.start_date
        self.end_date = challenge_page.end_date
        self.parse_error = False
        self.status_text = 'OK'
        self.parse_date = timezone.now()
        self.save(force_update=True)

        for comp_dict in challenge_page.competitors:
            external_id = comp_dict['external_id']

            competitor, _ = Competitor.objects.get_or_create(external_id=external_id)
            competitor.name = comp_dict['name']
            competitor.save()

            stats, _ = Stats.objects.get_or_create(challenge=self, competitor=competitor)
            stats.calories = comp_dict['calories']
            stats.save()

    def __str__(self):
        name = '"{}"'.format(self.title) if self.title else self.external_id
        return 'Challenge {}'.format(name)
