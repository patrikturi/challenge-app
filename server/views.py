from datetime import datetime

from flask import Blueprint, current_app as app

from server import database
from server.utils.query_util import QueryUtil

bp = Blueprint("views", __name__)

query_util = QueryUtil(database.session)


def _get_date():
    return app.config['MOCK_DATE'] if app.config.get('TESTING') else datetime.now()


@bp.route('/challenges/active')
def active_challenges():
    current_date = _get_date()
    data = [challenge.asdict() for challenge in query_util.get_active_challenges(current_date)]
    return {'success': True, 'data': data}


@bp.route('/challenges/inactive')
def inactive_challenges():
    current_date = _get_date()
    data = [challenge.asdict() for challenge in query_util.get_inactive_challenges(current_date)]
    return {'success': True, 'data': data}
