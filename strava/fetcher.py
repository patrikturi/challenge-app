from datetime import datetime
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from challenges.models import Challenge, ChallengeTypes, DataProviderType, Team, Stats, STRAVA_STAT_TYPES, StatTypes, StatUnits
from strava import strava_api
from strava.models.token import StravaToken


def fetch_all():
    records = _query_records()
    print(records)
    for record in records:
        _refresh_stats(record)


def _query_records():
    challenges = Challenge.objects.get_active(kind=ChallengeTypes.STRAVA)

    # Challenge - ExternalProfile - Token
    token_id_field = 'competitors__external_profiles__strava_tokens'
    values = Team.objects.filter(
        challenge__in=challenges,
        competitors__external_profiles__kind=DataProviderType.STRAVA
    ).values('challenge__start_date', 'challenge__end_date', 'competitors', 'competitors__external_profiles', token_id_field)
    token_ids = [val[token_id_field] for val in values]
    tokens = StravaToken.objects.filter(id__in=token_ids)

    return [
        {
            'start_date': val['challenge__start_date'],
            'end_date': val['challenge__end_date'],
            'athlete_id': val['competitors__external_profiles'],
            'token': tokens.get(id=val[token_id_field]),
            'competitor_id': val['competitors'],
        } for val in values
    ]


def _refresh_stats(record):
    token = record['token']
    start = timezone.make_aware(datetime.combine(record['start_date'], datetime.min.time()), timezone.utc)
    end = timezone.make_aware(datetime.combine(record['end_date'], datetime.max.time()), timezone.utc) if record['end_date'] else None
    activities = strava_api.get_activities(token.access_token, before=end.timestamp(), after=start.timestamp())

    stats = Stats.objects.filter(competitor_id=record['competitor_id'], kind__in=STRAVA_STAT_TYPES, external_datetime__gt=start, external_datetime__lt=end)

    activities = [a for a in activities if a['type'].upper() in STRAVA_STAT_TYPES]

    for activity in activities:
        Stats.objects.update_or_create(external_id=activity['id'], defaults={
            'competitor_id': record['competitor_id'],
            'value': int(activity['distance']),
            'kind': activity['type'].upper(),
            'external_datetime': parse_datetime(activity['start_date']),
            'unit': StatUnits.METERS,
            'external_id': activity['id'],
        })

    existing_ids = set(stat.external_id for stat in stats)
    received_ids = set(activity['id'] for activity in activities)

    missing_ids = existing_ids - received_ids
    if missing_ids:
        Stats.objects.filter(external_id__in=missing_ids).delete()
        # TODO: log delete, log skipping
