import os

from flask import Flask

import server.database


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('APP_SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    if not os.path.isdir(app.instance_path):
        os.makedirs(app.instance_path)

    from server.views import challenge_view
    challenge_view.register(app)
    from server.views import team_view
    team_view.register(app)
    from server.views import team_member_view
    team_member_view.register(app)

    from server import error_handlers
    error_handlers.register(app)

    return app
