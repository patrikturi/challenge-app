from django.db import models

from challenges.models import Team


class Competitor(models.Model):

    endomondo_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    display_name = models.CharField(max_length=100, blank=True, help_text='Optional, name will be parsed form endomondo.com if not specified')
    teams = models.ManyToManyField(Team, blank=True)

    def __str__(self):
        if self.display_name:
            name = '"{}"'.format(self.display_name)
        elif self.name:
            name = '"{}"'.format(self.name)
        else:
            name = self.endomondo_id
        return 'Competitor {}'.format(name)

    def get_name(self):
        if self.display_name:
            return self.display_name
        elif self.name:
            return self.name
        else:
            return 'Competitor {}'.format(self.endomondo_id)
