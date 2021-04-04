from datetime import timedelta

from django.db import models
from django.db.models import Q
from django.utils import timezone


class Challenge(models.Model):

    endomondo_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200, blank=True)
    start_date = models.DateField('Start date', null=True, blank=True)
    end_date = models.DateField('End date', null=True, blank=True)
    parse_error = models.NullBooleanField()
    status_text = models.CharField(max_length=200, default='-')
    parse_date = models.DateTimeField('Parse date', null=True, blank=True)

    def __str__(self):
        name = '"{}"'.format(self.title) if self.title else self.endomondo_id
        return 'Challenge {}'.format(name)

    @classmethod
    def get_last(cls, now):
        active_challenges = Challenge.objects.filter( \
            Q(start_date__lte=now, end_date__gte=now) | Q(start_date__isnull=True)) \
            .order_by('-start_date')

        if len(active_challenges) > 0:
            challenge = active_challenges[0]
        else:
            challenges_ended = Challenge.objects.filter(end_date__lt=now).order_by('-end_date')
            if len(challenges_ended) > 0:
                challenge = challenges_ended[0]
            else:
                challenge = None
        return challenge

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
            endomondo_id = comp_dict['endomondo_id']

            comptetitor = Competitor.get_or_create(endomondo_id)
            comptetitor.name = comp_dict['name']
            comptetitor.save()

            stats = Stats.get_or_create(challenge=self, competitor=comptetitor)
            stats.calories = comp_dict['calories']
            stats.save()

    @classmethod
    def get_non_final(cls):
        """These challenges will be updated from endomondo.com"""
        # Upcoming or Ongoing or Completed just lately
        end = timezone.now() - timedelta(days=1)
        challenges = Challenge.objects.filter(Q(end_date__gt=end) | Q(end_date__isnull=True)).order_by('-start_date')
        return challenges
