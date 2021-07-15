import json
import requests
import time
import os

from django.conf import settings

STRAVA_OAUTH_URL = 'http://www.strava.com/oauth'
STRAVA_API_URL = 'https://www.strava.com/api/v3'


def get_auth_uri():
    redirect_uri = f'{settings.HOSTNAME}/strava/token-exchange'
    scope = 'activity:read'
    prompt = 'force'
    auth_uri = f'{STRAVA_OAUTH_URL}/authorize?client_id={settings.STRAVA_CLIENT_ID}&response_type=code&redirect_uri={redirect_uri}&approval_prompt={prompt}&scope={scope}'
    return auth_uri


def get_token(grant_type, code):
    token_exchange_data = {
        'client_id': settings.STRAVA_CLIENT_ID,
        'client_secret': settings.STRAVA_SECRET,
        'grant_type': grant_type,
        'code': code,
    }
    if grant_type == 'authorization_code':
        token_exchange_data['code'] = code
    else:
        token_exchange_data['refresh_token'] = code

    resp = requests.post(url=f'{STRAVA_OAUTH_URL}/token', data=token_exchange_data)

    return resp.json()


def get_activities(access_token):
    resp = requests.get(f'{STRAVA_API_URL}/activities', headers={
        'Authorization': f'Bearer {access_token}'
    })
    return resp.json()
