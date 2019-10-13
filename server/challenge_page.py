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
            id = int(user['href'].split('/')[-1])
            kcal = self._get_user_kcal(id)
            users.append((name, id, kcal))
        return users

    def _get_page_url(self, css_class):
        anchors = self.soup.find_all('a', class_=' '.join(['increment', css_class]))
        # TODO: log error
        # If the page does not exist we get <span> instead of <a>
        assert len(anchors) <= 1
        if not anchors:
            return None
        anchor = anchors[0]
        href = anchor.get('href')
        if not href or len(href) < 2:
            return None
        # Remove the initial '..' from the url
        return href[2:]

    def _anchor_of_user(self, anchors, user_id):
        for a in anchors:
            if a.get('href') == f'../profile/{user_id}':
                return a
        return None

    def _get_user_kcal(self, user_id):
        anchors = self.soup.select('.chart-row .bar a')
        anchor = self._anchor_of_user(anchors, user_id)

        # FIXME: not found/parse error: log and continue
        kcal_div = anchor.parent.find_next_sibling('div')
        # replaces non-breakable space with space
        kcal_str = unicodedata.normalize('NFKD', kcal_div.text)
        # eg. "123 kcal"
        return int(kcal_str.split(' ')[0])
