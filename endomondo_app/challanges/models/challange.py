from django.db import models
from django.db.models import Q
from django.forms.models import model_to_dict


class Challange(models.Model):

    endomondo_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200, blank=True)
    start_date = models.DateTimeField('Start date', null=True, blank=True)
    end_date = models.DateTimeField('End date', null=True, blank=True)

    def to_short_dict(self):
        return {'id': self.id, 'title': self.title, 'start_date': self.start_date}

    # View of the model. Would be better to use eg. restframework but this was the lowest effort
    def to_dict(self):
        # Avoids circular imports
        from challanges.models.team import Team
        from challanges.models.competitor import Competitor
        from challanges.models.stats import Stats

        teams = Team.objects.filter(challange=self)
        team_dicts = [team.to_dict() for team in teams]
 
        challange_dict = model_to_dict(self)
        challange_dict['teams'] = team_dicts
        return challange_dict

    def __str__(self):
        name = '"{}"'.format(self.title) if self.title else self.endomondo_id
        return 'Challange {}'.format(name)

    @classmethod
    def get_last(cls, now):
        active_challanges = Challange.objects.filter( \
            Q(start_date__lt=now, end_date__gt=now) | Q(start_date__isnull=True)) \
            .order_by('-start_date')

        if len(active_challanges) > 0:
            challange = active_challanges[0]
        else:
            challanges_ended = Challange.objects.filter(end_date__lt=now).order_by('-end_date')
            if len(challanges_ended) > 0:
                challange = challanges_ended[0]
            else:
                challange = None
        return challange

    def update(self, challenge_page):
        from challanges.models.competitor import Competitor
        from challanges.models.stats import Stats

        self.title = challenge_page.name
        self.start_date = challenge_page.start_date
        self.end_date = challenge_page.end_date
        self.save(force_update=True)

        for comp_dict in challenge_page.competitors:
            endomondo_id = comp_dict['endomondo_id']

            comptetitor = Competitor.get_or_create(endomondo_id)
            comptetitor.name = comp_dict['name']
            comptetitor.save()

            stats = Stats.get_or_create(challenge=self, competitor=comptetitor)
            stats.calories = comp_dict['calories']
            stats.save()
