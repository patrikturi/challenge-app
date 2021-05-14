from rest_framework.response import Response
from rest_framework.status import HTTP_302_FOUND
from rest_framework.views import APIView

from challenges.models.external_profile import ExternalProfile
from strava import strava_api
from strava.models.token import StravaToken


class ExchangeToken(APIView):

    def get(self, request):
        code = request.GET['code']
        scope = request.GET['scope']
        if scope != 'read,activity:read':
            return 'ERROR: Authorization to reading activities is strictly required to participate!'
        token_data = strava_api.get_token('authorization_code', code)

        athlete_id = token_data['athlete']['id']
        profile = ExternalProfile.get_or_create(external_id=athlete_id)
        profile.name = token_data['athlete']['firstname'] + ' ' + token_data['athlete']['lastname']
        token = StravaToken.get_or_create(profile=profile)

        token.access_token = token_data['access_token']
        token.refresh_token = token_data['refresh_token']
        token.expires_at = token_data['expires_at']
        token.save()

        return Response("/", status=HTTP_302_FOUND)
