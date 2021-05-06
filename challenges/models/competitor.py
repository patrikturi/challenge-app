from django.db import models

from challenges.models import Team


class Competitor(models.Model):

    display_name = models.CharField(max_length=100, blank=True)
    teams = models.ManyToManyField(Team, related_name='competitors', blank=True)

    def __str__(self):
        if self.display_name:
            name = '"{}"'.format(self.display_name)
        else:
            name = self.external_id
        return 'Competitor {}'.format(name)

    def get_name(self):
        if self.display_name:
            return self.display_name
        else:
            return 'Competitor {}'.format(self.external_id)
