from django.conf import settings


class DataProvider:

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

    def to_representation(self):
        return {
            'name': self.get_name(),
            'url': self.get_url(),
            'logo_url': self.get_logo_url()
        }


class DummyProvider(DataProvider):
    """Used in unit tests"""

    def get_name(self):
        return 'Unknown'

    def get_url(self):
        return 'https://example.com'

    def get_challenge_url(self, external_id):
        return f'https://example.com/challenges/{external_id}'

    def get_competitor_url(self, external_id):
        return f'https://example.com/profile/{external_id}'


class EndomondoProvider(DataProvider):

    def get_name(self):
        return 'Endomondo'

    def get_url(self):
        return 'https://endomondo.com'

    def get_challenge_url(self, external_id):
        return f'https://endomondo.com/challenges/{external_id}'

    def get_competitor_url(self, external_id):
        return f'https://endomondo.com/profile/{external_id}'


class StravaProvider(DataProvider):

    def get_name(self):
        return 'Strava'

    def get_url(self):
        return 'https://strava.com'

    def get_challenge_url(self, external_id):
        return None

    def get_competitor_url(self, external_id):
        return f'https://strava.com/athletes/{external_id}'
