from datetime import datetime

from bs4 import BeautifulSoup

from challanges.models.competitor import Competitor


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
    def title(self):
        title_element = self.soup.find('title')
        # exmaple: "Challenge Title! - 2019 | Most calories (All sports) Challenge | Endomondo"
        return title_element.text.split(' | ')[0].strip()

    @property
    def competitors(self):
        elements = self.soup.find_all('a', class_='name')
        competitors = []
        for element in elements:
            id = int(element['href'].split('/')[-1])
            competitors.append({
                'name': element.text,
                'endomondo_id': id,
                'calories': self._parse_calories(id)
            })
        return competitors

    @property
    def start_date(self):
        return self._get_date('start')

    @property
    def end_date(self):
        return self._get_date('end')

    def _get_date(self, class_name):
        # Get start or end date
        div = self.soup.find('div', class_=class_name)
        date_span = div.findChild('span').find_next_sibling('span')
        return datetime.strptime(date_span.text, "%b %d, %Y %I:%M %p").date()

    def _get_page_url(self, css_class):
        anchors = self.soup.find_all('a', class_=' '.join(['increment', css_class]))
        assert len(anchors) <= 1
        # If the next/previous page does not exist we get <span> instead of <a>
        if not anchors:
            return None
        url = anchors[0]['href']
        # Remove the initial '..' from the relative url
        return url[2:]

    def _get_profile_anchor(self, anchors, id):
        for a in anchors:
            if a.get('href') == f'../profile/{id}':
                return a
        return None

    def _parse_calories(self, id):
        anchors = self.soup.select('.chart-row .bar a')
        anchor = self._get_profile_anchor(anchors, id)

        calories_div = anchor.parent.find_next_sibling('div')
        # replace non-breakable space with space
        calories_str = calories_div.text.replace('\xa0', ' ')
        # eg. "123 kcal"
        if 'Challenge not started' in calories_str or 'No applicable workouts' in calories_str:
            return 0
        calories = calories_str.split(' ')[0]
        if not calories.isdigit():
            raise ValueError(f'Expected "<integer> kcal" for calories, got: "{calories_str}"')
        return int(calories)
