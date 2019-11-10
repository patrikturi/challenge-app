from server.challenge_page import ChallengePage


class BackgroundService:

    def __init__(self, endomondo_api, query_util):
        self.endomondo_api = endomondo_api
        self.query_util = query_util

    def fetch_active_challenges(self, current_date):

        challenges = self.query_util.get_active_challenges(current_date)

        for challenge in challenges:
            page_data = self.endomondo_api.get_page(f'http://endomondo.com/challenges/{challenge.endomondo_id}')
            # FIXME: walk prev/next pages
            page = ChallengePage(page_data)
            challenge.update(page)
