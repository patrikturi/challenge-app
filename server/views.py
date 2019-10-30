from flask import Blueprint, current_app as app
from datetime import datetime

from server import CompetitorRepository, database, ChallengeRepository

bp = Blueprint("views", __name__)

competitor_repo = CompetitorRepository(database.session)
challenge_repo = ChallengeRepository(database.session, competitor_repo)


@bp.route('/challenges/active')
def active_challenges():

    current_date = app.config['MOCK_DATE'] if app.config.get('TESTING') else datetime.now()

    data = [challenge.asdict() for challenge in challenge_repo.get_all_active(current_date)]
    return {'success': True, 'data': data}
