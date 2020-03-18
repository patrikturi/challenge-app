from collections import Counter

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.db.models import Q 

from challenges.models.challenge import Challenge
from challenges.models.team import Team
from challenges.models.competitor import Competitor


class ChallengeAdmin(admin.ModelAdmin):
    fields = ('endomondo_id', 'endomondo_link', 'site_link', 'competitors_without_team')
    readonly_fields = ('endomondo_link', 'site_link', 'competitors_without_team', )

    def endomondo_link(self, obj):
        return mark_safe('<a href="https://www.endomondo.com/challenges/{}">Endomondo link</a>'.format(obj.endomondo_id))

    def site_link(self, obj):
        return mark_safe('<a href="/challenge/{}/">Site link</a>'.format(obj.id))

    def competitors_without_team(self, obj):
        # Has Stats in Ch but no Team in Ch
        comps = Competitor.objects.filter(~Q(teams__challenge=obj) & Q(stats__challenge=obj))
        comp_entries = []
        for comp in comps:
            entry = '<div><a href="/admin/challenges/competitor/{id}/change/">{name}</a></div>'.format(id=comp.id, name=str(comp))
            comp_entries.append(entry)
        html = ''.join(comp_entries) if comp_entries else '-'
        return mark_safe(html)


class CompetitorForm(forms.ModelForm):

    def _get_first_duplicates(self, counter):
        for item, count in counter.items():
            if count > 1:
                return item
        return None

    def clean(self):
        """
        This is the function that can be used to 
        validate your model data from admin
        """
        super().clean()
        teams = self.cleaned_data.get('teams')

        challenge_ids = Counter([team.challenge.id for team in teams])
        duplicate_id = self._get_first_duplicates(challenge_ids)
        if duplicate_id is not None:
            duplicate_names = [team.name for team in teams if team.challenge.id == duplicate_id]
            duplicate_names_quoted = ['"{}"'.format(name) for name in duplicate_names]
            duplicate_names_str = ', '.join(duplicate_names_quoted)
            raise ValidationError('The following teams are in the same challenge: {}'.format(duplicate_names_str))


class CompetitorAdmin(admin.ModelAdmin):
    fields = ('display_name', 'teams')
    form = CompetitorForm

    # Competitors are parsed/created from Endomondo, it is not needed to create them manually
    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Team)
admin.site.register(Competitor, CompetitorAdmin)
