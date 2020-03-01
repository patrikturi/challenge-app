from django.contrib import admin

from challanges.models.challange import Challange
from challanges.models.team import Team
from challanges.models.competitor import Competitor


class ChallangeAdmin(admin.ModelAdmin):
    fields = ('endomondo_id',)


class CompetitorAdmin(admin.ModelAdmin):
    fields = ('endomondo_id', 'display_name', 'teams')


admin.site.register(Challange, ChallangeAdmin)
admin.site.register(Team)
admin.site.register(Competitor, CompetitorAdmin)
