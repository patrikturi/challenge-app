from requests import HTTPError

from challenges.models.challenge import Challenge
from challenges.endomondo.api import EndomondoApi
from challenges.endomondo.challenge_page import ChallengePage
from mysite import settings
from django.http import HttpResponse


api = EndomondoApi()


def process_page(api, ch, url):
    # TODO catch invalid challenge id
    html = api.get_page(url)
    with open('out.html', 'w') as file:
        file.write(html)
    page = ChallengePage(html)
    ch.update(page)
    return page


def fetch_challenges(request):       
    api.login(settings.ENDOMONDO_USERNAME, settings.ENDOMONDO_PASSWORD)

    challenges = Challenge.get_non_final()

    for ch in challenges:
        orig_page = None
        try:
            print('Updating challenge: {}'.format(ch.endomondo_id))
            url = 'https://www.endomondo.com/challenges/{}'.format(ch.endomondo_id)
            orig_page = process_page(api, ch, url)
        except HTTPError as e:
            if e.response.status_code == 404:
                print('404')
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
                prev_url = page.prev_page_url
        return HttpResponse()