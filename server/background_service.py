from server.challenge_page import ChallengePage


class BackgroundService:

    def __init__(self, challenge_repository):
        self.challenge_repository = challenge_repository

    def fetch_active_challenges(self, endomondo_api, current_date):

        challenges = self.challenge_repository.get_all_active(current_date)

        for challenge in challenges:
            page_data = endomondo_api.get_page(f'http://endomondo.com/challenges/{challenge.endomondo_id}')
            page = ChallengePage(page_data)
            self.challenge_repository.update(challenge.endomondo_id, page)
