from django.db import models

from challanges.models.challange import Challange
from challanges.models.competitor import Competitor


class Stats(models.Model):
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE)
    challange = models.ForeignKey(Challange, on_delete=models.CASCADE)
    calories = models.IntegerField()
