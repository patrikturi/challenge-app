from bs4 import BeautifulSoup
import unicodedata


class ChallengePage:
    """Single page of a Challenge on endomondo.com"""

    def __init__(self, html_string):
        self.soup = BeautifulSoup(html_string, 'html.parser')

    @property
    def next_page_url(self):
        return self._get_page_url('next')

    @property
    def prev_page_url(self):
        return self._get_page_url('prev')

    @property
    def users(self):
        user_elements = self.soup.find_all('a', class_='name')
        users = []
        for user in user_elements:
            name = user.text
            id = user['href'].split('/')[-1]
            calories = self._get_calories(id)
            users.append((name, id, calories))
        return users

    def _get_page_url(self, css_class):
        anchors = self.soup.find_all('a', class_=' '.join(['increment', css_class]))
        assert len(anchors) <= 1
        # If the next/previous page does not exist we get <span> instead of <a>
        if not anchors:
            return None
        url = anchors[0]['href']
        # Remove the initial '..' from the relative url
        return url[2:]

    def _get_anchor(self, anchors, user_id):
        for a in anchors:
            if a.get('href') == f'../profile/{user_id}':
                return a
        return None

    def _get_calories(self, user_id):
        anchors = self.soup.select('.chart-row .bar a')
        anchor = self._get_anchor(anchors, user_id)

        calories_div = anchor.parent.find_next_sibling('div')
        # replaces non-breakable space with space
        calories_str = unicodedata.normalize('NFKD', calories_div.text)
        # eg. "123 kcal"
        if 'challenge not started' in calories_str.lower():
            return 0
        calories = calories_str.split(' ')[0]
        if not calories.isdigit():
            raise ValueError(f'Expected "<integer> kcal" for calories, got: "{calories_str}"')
        return int(calories)
