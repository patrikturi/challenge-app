from django.db import models

from challanges.models.challange import Challange

class Team(models.Model):

    name = models.CharField(max_length=100)
    challange = models.ForeignKey(Challange, on_delete=models.CASCADE)
