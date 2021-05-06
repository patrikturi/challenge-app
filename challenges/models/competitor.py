from django.db import models

from challenges.models import Team


class Competitor(models.Model):

    external_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    display_name = models.CharField(max_length=100, blank=True, help_text=f'Optional, name will be parsed form the data external site if not specified')
    teams = models.ManyToManyField(Team, related_name='competitors', blank=True)

    def __str__(self):
        if self.display_name:
            name = '"{}"'.format(self.display_name)
        elif self.name:
            name = '"{}"'.format(self.name)
        else:
            name = self.external_id
        return 'Competitor {}'.format(name)

    def get_name(self):
        if self.display_name:
            return self.display_name
        elif self.name:
            return self.name
        else:
            return 'Competitor {}'.format(self.external_id)
