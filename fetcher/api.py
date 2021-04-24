import requests
from fetcher.loggers import fetch_logger


ENDOMONDO_URL = 'https://www.endomondo.com'
ENDOMONDO_LOGIN_URL = ENDOMONDO_URL + '/rest/session'

# Currently Endomondo REST API does not exist for Challenges
# so the necessary http requests have been reverse engineered
# from the browser
class EndomondoApi:

    def __init__(self):
        # We get 403 Forbidden response without specifying a real User-Agent
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }
        self.session = requests.Session()

    def login(self, username, password):
        # Check if logged in, acquire CSRF token
        if 'x-csrf-token' in self.headers:
            resp = self.session.get(ENDOMONDO_LOGIN_URL, headers=self.headers)
            if resp.ok:
                # Already logged in
                fetch_logger.info('Already logged in')
                return

        resp = self.session.get(ENDOMONDO_URL, headers=self.headers)
        resp.raise_for_status()
        self.headers['x-csrf-token'] = self.session.cookies['CSRF_TOKEN']
        fetch_logger.info('Logging in')

        # Post login data
        data = {'email': username, 'password': password}
        resp = self.session.post(ENDOMONDO_LOGIN_URL, headers=self.headers, json=data)
        resp.raise_for_status()

    def get_page(self, url):
        domain_name = 'endomondo.com'
        if not domain_name in url.lower():
            raise ValueError(f'Invalid URL "{url}", the url must be on {domain_name}')
        fetch_logger.info(f'Getting page {url}')
        resp = self.session.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.text
