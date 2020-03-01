import os
import time

from challanges.endomondo.api import EndomondoApi


def test_getPage_fetchesChallengePage():
    username = 'mentor.endomondo@gmail.com'
    url = 'https://www.endomondo.com/challenges/41375412'
    password = os.environ['ENDOMONDO_USER_PASSWORD']

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
