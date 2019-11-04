import argparse
import os

from server.endomondo_api import EndomondoApi


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('username', help='Username (email address) on endomondo.com')
    parser.add_argument('url', help='URL to load')
    args = parser.parse_args()

    password = os.environ['ENDOMONDO_USER_PASSWORD']
    api = EndomondoApi()
    api.login(args.username, password)
    body = api.get_page(args.url)
    print(body)
