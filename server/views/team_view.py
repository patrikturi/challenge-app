from flask.views import MethodView
from flask import request

from server import database
from server.utils.repository_util import RepositoryUtil

repo_util = RepositoryUtil(database.session)


class TeamView(MethodView):

    def post(self):
        challenge_id = request.json.get('challenge_id')
        team_name = request.json.get('team_name')

        repo_util.insert_team(team_name, challenge_id)


def register(app_instance):
    team_view = TeamView.as_view('team_view')
    app_instance.add_url_rule('/team', view_func=team_view, methods=['GET', 'POST'])
