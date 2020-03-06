from django.db import models
from django.forms.models import model_to_dict

from challanges.models.team import Team


class Competitor(models.Model):

    endomondo_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    display_name = models.CharField(max_length=100, blank=True, help_text='Optional, name will be parsed form endomondo.com if not specified')
    teams = models.ManyToManyField(Team, blank=True)

    def to_dict(self, challange_id):
        from challanges.models.stats import Stats

        self_dict = model_to_dict(self)
        if self.display_name:
            self_dict['name'] = self.display_name

        del self_dict['display_name']
        del self_dict['teams']

        try:
            stats = Stats.objects.get(challange__id=challange_id, competitor__id=self.id)
            self_dict['calories'] = stats.calories
        except Stats.DoesNotExist:
            self_dict['calories'] = 0

        return self_dict

    def __str__(self):
        if self.display_name:
            name = '"{}"'.format(self.display_name)
        elif self.name:
            name = '"{}"'.format(self.name)
        else:
            name = self.endomondo_id
        return 'Competitor {}'.format(name)

    @classmethod
    def get_or_create(cls, endomondo_id):
        try:
            return Competitor.objects.get(endomondo_id=endomondo_id)
        except Competitor.DoesNotExist:
            return Competitor(endomondo_id=endomondo_id)
