from flask.views import MethodView
from flask import request

from server import database
from server.utils.repository_util import RepositoryUtil

repo_util = RepositoryUtil(database.session)


class TeamMemberView(MethodView):

    def post(self):
        team_id = request.json.get('team_id')
        competitor_id = request.json.get('competitor_id')

        repo_util.insert_team_member(team_id, competitor_id)

    def delete(self):
        team_id = request.json.get('team_id')
        competitor_id = request.json.get('competitor_id')

        repo_util.remove_team_member(team_id, competitor_id)

def register(app_instance):
    team_member_view = TeamMemberView.as_view('team_member_view')
    app_instance.add_url_rule('/team/member', view_func=team_member_view, methods=['POST', 'DELETE'])
