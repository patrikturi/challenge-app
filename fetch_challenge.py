import requests
from bs4 import BeautifulSoup

import os

HOMEPAGE_URL = 'https://www.endomondo.com'
CHALLENGE_URL = 'https://www.endomondo.com/challenges/41375412'


'''
 Currently Endomondo REST API does not exist for Challenges
 so the necessary http requests have been reverse engineered
 from the browser
'''

session = requests.Session()

initial_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}

print('Get csrf token')
resp = session.get(HOMEPAGE_URL, headers=initial_headers)
print(f'get: {resp}')


all_headers = {
    'x-csrf-token': session.cookies['CSRF_TOKEN']
}
all_headers.update(initial_headers)

print('Login')
data = {'email': os.environ['ENDOMONDO_USER_EMAIL'], 'password': os.environ['ENDOMONDO_USER_PASSWORD'], 'remember': False}
resp = session.post('https://www.endomondo.com/rest/session', headers=all_headers, json=data)
print(f'post: {resp}')


print('Get Challenge initial page')
resp = session.get('https://www.endomondo.com/challenges/41375412', headers=all_headers)
print(f'resp: {resp}')
with open('out.html', 'w') as file:
    file.write(resp.text)


# Get prev page URL
with open('out.html', 'r') as file:
    html_doc = file.read()

soup = BeautifulSoup(html_doc, 'html.parser')

# TODO: same for next page, until the end is reached
anchors = soup.find_all('a', class_='increment prev')
assert len(anchors) == 1
prev_page_href = HOMEPAGE_URL + '/' + anchors[0]['href'][3:]

print('Get Challenge prev page')
print(prev_page_href)

resp = session.get(prev_page_href, headers=all_headers)
print(f'resp: {resp}')
with open('out2.html', 'w') as file:
    file.write(resp.text)
