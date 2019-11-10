from datetime import datetime
from flask.views import MethodView
from flask import current_app as app
from flask import request

from server import database
from server.utils.query_util import QueryUtil

query_util = QueryUtil(database.session)


def _get_date():
    return app.config['MOCK_DATE'] if app.config.get('TESTING') else datetime.now()


class ChallengeView(MethodView):

    def get(self):
        active = request.args.get('active', 'true')
        active = isinstance(active, str) and active.lower() == 'true'
        get_challenges = query_util.get_active_challenges if active else query_util.get_inactive_challenges
        current_date = _get_date()
        data = [challenge.asdict() for challenge in get_challenges(current_date)]
        return {'success': True, 'data': data}


def register(app_instance):
    challenge_view = ChallengeView.as_view('challenge_view')
    app_instance.add_url_rule('/challenges', view_func=challenge_view, methods=['GET', ])
