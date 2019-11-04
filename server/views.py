from flask import Blueprint, current_app as app
from datetime import datetime

from server import CompetitorRepository, database, ChallengeRepository
from server.calories_repository import CaloriesRepository

bp = Blueprint("views", __name__)

competitor_repo = CompetitorRepository(database.session)
calories_repo = CaloriesRepository(database.session)
challenge_repo = ChallengeRepository(database.session, competitor_repo, calories_repo)


def _get_date():
    return app.config['MOCK_DATE'] if app.config.get('TESTING') else datetime.now()


@bp.route('/challenges/active')
def active_challenges():
    current_date = _get_date()
    data = [challenge.asdict() for challenge in challenge_repo.get_all_active(current_date)]
    return {'success': True, 'data': data}


@bp.route('/challenges/inactive')
def inactive_challenges():
    current_date = _get_date()
    data = [challenge.asdict() for challenge in challenge_repo.get_all_inactive(current_date)]
    return {'success': True, 'data': data}
