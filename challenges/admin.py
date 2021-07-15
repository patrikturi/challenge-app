from collections import Counter
from strava.models.token import StravaToken

from django import forms
from django.contrib import admin
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.db.models import Q

from challenges.models import Challenge, Competitor, Team, ExternalProfile, ChallengeTypes, DataProviderType


class ChallengeForm(forms.ModelForm):

    def clean(self):
        super().clean()
        ch = self.instance
        is_kind_changed = ch and ch.kind != self.cleaned_data.get('kind')
        if (not ch or is_kind_changed) and self.cleaned_data.get('kind') == ChallengeTypes.ENDOMONDO.value:
            raise ValidationError('Endomondo is no longer supported')


class ChallengeAdmin(admin.ModelAdmin):
    fields = ('external_id', 'title', 'start_date', 'end_date', 'external_link', 'site_link', 'competitors_without_team', 'status', 'kind')
    readonly_fields = ('external_link', 'site_link', 'competitors_without_team', 'status' )
    form = ChallengeForm

    def external_link(self, obj):
        return mark_safe('<a href="{}">{} link</a>'.format(obj.external_url, obj.kind)) if obj.external_url else '-'

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

    def status(self, obj):
        status_class = ' style="color:red"' if obj.parse_error else ''
        html = '<span{}>{}</span>'.format(status_class, obj.status_text)
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


class ExternalProfileForm(forms.ModelForm):

    def clean(self):
        super().clean()
        p = self.instance
        is_kind_changed = p and p.kind != self.cleaned_data.get('kind')
        if (not p or is_kind_changed) and self.cleaned_data.get('kind') == DataProviderType.ENDOMONDO.value:
            raise ValidationError('Endomondo is no longer supported')


class ExternalProfileInline(admin.StackedInline):
    model = ExternalProfile
    fields = ('external_id', 'kind')
    form = ExternalProfileForm
    extra = 1

class CompetitorAdmin(admin.ModelAdmin):
    fields = ('display_name', 'teams')
    form = CompetitorForm
    inlines = [ExternalProfileInline]


admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Team)
admin.site.register(Competitor, CompetitorAdmin)
admin.site.register(StravaToken)
