from django.db import models
from django.forms.models import model_to_dict

from challanges.models.team import Team


class Competitor(models.Model):

    endomondo_id = models.IntegerField()
    name = models.CharField(max_length=100, blank=True)
    display_name = models.CharField(max_length=100, blank=True, help_text='Optional, name will be parsed form endomondo.com if not specified')
    teams = models.ManyToManyField(Team, blank=True)

    def to_dict(self):
        self_dict = model_to_dict(self)
        if self.display_name:
            self_dict['name'] = self.display_name
        del self_dict['display_name']
        return self_dict

    def __str__(self):
        if self.display_name:
            name = '"{}"'.format(self.display_name)
        elif self.name:
            name = '"{}"'.format(self.name)
        else:
            name = self.endomondo_id
        return 'Competitor {}'.format(name)
