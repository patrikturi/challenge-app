import os
import time

from challenges.endomondo.api import EndomondoApi


def test_getPage_fetchesChallengePage():
    url = 'https://www.endomondo.com/challenges/41375412'
    username = os.environ['ENDOMONDO_USER']
    password = os.environ['ENDOMONDO_PASSWORD']

    api = EndomondoApi()
    api.login(username, password)
    body = api.get_page(url)
    motto = 'Fun, Health, Friendship, BeachBody, Sport, Teambuilding'
    if motto not in body:
        raise AssertionError()


if __name__ == '__main__':
    start_time = time.time()
    test_getPage_fetchesChallengePage()
    end_time = time.time()
    print('OK {:.2f} sec'.format(end_time-start_time))
