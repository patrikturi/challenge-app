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

    def get_active(self, kind):
        now = timezone.now()
        challenges = self.filter((Q(end_date__gte=now) | Q(end_date__isnull=True)) & Q(start_date__lte=now), kind=kind).order_by('-start_date')
        return challenges


class ChallengeTypes(models.TextChoices):
    ENDOMONDO = 'ENDOMONDO', 'kcal', False
    STRAVA = 'STRAVA', 'km', True

    def __new__(cls, svalue, score_units, enabled):
        obj = str.__new__(cls, svalue)
        obj._value_ = svalue
        obj.score_units = score_units
        obj.enabled = enabled
        return obj

    @classmethod
    def get_provider(cls, challenge_type):
        from challenges.providers import EndomondoProvider, StravaProvider, DummyProvider
        if challenge_type == cls.ENDOMONDO.value:
            return EndomondoProvider()
        elif challenge_type == cls.STRAVA.value:
            return StravaProvider()
        else:
            return DummyProvider()


class Challenge(models.Model):

    external_id = models.IntegerField(unique=True)
    kind = models.CharField(max_length=16, choices=ChallengeTypes.choices)
    title = models.CharField(max_length=200, blank=True)
    start_date = models.DateField('Start date', null=True, blank=True)
    end_date = models.DateField('End date', null=True, blank=True)
    parse_error = models.NullBooleanField()
    status_text = models.CharField(max_length=200, default='-')
    parse_date = models.DateTimeField('Parse date', null=True, blank=True)
    objects = ChallengeManager()

    def update(self, challenge_page):
        from challenges.models import Competitor, Stats, ExternalProfile

        self.title = challenge_page.title
        self.start_date = challenge_page.start_date
        self.end_date = challenge_page.end_date
        self.parse_error = False
        self.status_text = 'OK'
        self.parse_date = timezone.now()
        self.save(force_update=True)

        provider_type = self.provider.get_type()

        for comp_dict in challenge_page.competitors:
            external_id = comp_dict['external_id']

            profile = ExternalProfile.objects.get(external_id=external_id, kind=provider_type)
            profile.name = comp_dict['name']
            profile.save()

            stats, _ = Stats.objects.get_or_create(challenge=self, competitor_id=profile.competitor_id)
            stats.value = comp_dict['calories']
            stats.save()

    @property
    def provider(self):
        return ChallengeTypes.get_provider(self.kind)

    @property
    def score_units(self):
        return ChallengeTypes[self.kind].score_units

    @property
    def external_url(self):
        return self.provider.get_challenge_url(self.external_id)

    def __str__(self):
        name = '"{}"'.format(self.title) if self.title else self.external_id
        return 'Challenge {}'.format(name)
