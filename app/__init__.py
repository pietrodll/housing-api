import os
from flask import Flask
from flask_jwt import JWT
from .utils.errors import APIError


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)

    except OSError:
        pass

    # a simple page that says hello
    @app.route('/healthcheck')
    def healthcheck():
        return 'Hello World!'

    from . import auth
    app.register_blueprint(auth.bp)

    jwt = JWT(app, auth.authenticate, auth.identity)

    from .routes import user
    app.register_blueprint(user.bp)

    app.register_error_handler(APIError, APIError.to_json)

    return app
