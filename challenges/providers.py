from django.conf import settings
from challenges.models import DataProviderType
from strava import strava_api


class DataProvider:

    def get_type(self):
        raise NotImplementedError()

    def get_name(self):
        raise NotImplementedError()

    def get_url(self):
        raise NotImplementedError()

    def get_challenge_url(self, external_id):
        raise NotImplementedError()

    def get_competitor_url(self, external_id):
        raise NotImplementedError()

    def get_logo_url(self):
        return settings.STATIC_URL + f'img/{self.get_name().lower()}-logo.png'

    def get_template_name(self):
        return 'challenge.html'

    def to_representation(self):
        return {
            'name': self.get_name(),
            'url': self.get_url(),
            'logo_url': self.get_logo_url()
        }


class DummyProvider(DataProvider):
    """Used in unit tests"""

    def get_type(self):
        return 'Dummy'

    def get_name(self):
        return 'Unknown'

    def get_url(self):
        return 'https://example.com'

    def get_challenge_url(self, external_id):
        return f'https://example.com/challenges/{external_id}'

    def get_competitor_url(self, external_id):
        return f'https://example.com/profile/{external_id}'


class EndomondoProvider(DataProvider):

    def get_type(self):
        return DataProviderType.ENDOMONDO

    def get_name(self):
        return 'Endomondo'

    def get_url(self):
        return 'https://endomondo.com'

    def get_challenge_url(self, external_id):
        return f'https://endomondo.com/challenges/{external_id}'

    def get_competitor_url(self, external_id):
        return f'https://endomondo.com/profile/{external_id}'


class StravaProvider(DataProvider):

    def get_type(self):
        return DataProviderType.STRAVA

    def get_name(self):
        return 'Strava'

    def get_url(self):
        return 'https://strava.com'

    def get_challenge_url(self, external_id):
        return None

    def get_competitor_url(self, external_id):
        return f'https://strava.com/athletes/{external_id}'

    def get_template_name(self):
        return 'strava_challenge.html'

    def to_representation(self):
        repr = super().to_representation()
        repr['auth_uri'] = strava_api.get_auth_uri()
        return repr
