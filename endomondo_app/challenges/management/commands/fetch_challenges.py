from requests import HTTPError
from challenges.models.challenge import Challenge
from challenges.endomondo.api import EndomondoApi
from challenges.endomondo.challenge_page import ChallengePage
from django.conf import settings
from django.http import HttpResponse
from django.core.management.base import BaseCommand

from challenges.loggers import fetch_logger


class Command(BaseCommand):
    help = 'Fetches active challenges from endomondo.com'

    def handle(self, *args, **options):
        api = EndomondoApi()

        challenges = Challenge.get_non_final()

        if challenges:
            api.login(settings.ENDOMONDO_USERNAME, settings.ENDOMONDO_PASSWORD)

        for ch in challenges:
            orig_page = None
            try:

                fetch_logger.info('Updating challenge: {}'.format(ch.endomondo_id))
                url = 'https://www.endomondo.com/challenges/{}'.format(ch.endomondo_id)
                orig_page = process_page(api, ch, url)
            except HTTPError as e:
                if e.response.status_code == 404:
                    fetch_logger.info('Challenge not found')
                    ch.parse_error = True
                    ch.status_text = 'NOT FOUND'
                    ch.save()
                else:
                    raise e
            else:
                prev_url = orig_page.prev_page_url
                while prev_url is not None:
                    page = process_page(api, ch, prev_url)
                    prev_url = page.prev_page_url

                next_url = orig_page.next_page_url
                while next_url is not None:
                    page = process_page(api, ch, next_url)
                    next_url = page.next_page_url

        fetch_logger.info('Completed')


def process_page(api, ch, url):
    html = api.get_page(url)
    page = ChallengePage(html)
    ch.update(page)
    return page
