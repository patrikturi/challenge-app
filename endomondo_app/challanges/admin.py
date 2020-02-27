from django.contrib import admin

from challanges.models.challange import Challange
from challanges.models.team import Team
from challanges.models.competitor import Competitor


admin.site.register(Challange)
admin.site.register(Team)
admin.site.register(Competitor)
