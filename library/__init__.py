import os
import pprint

from flask import (
    Flask, request
)

from werkzeug.exceptions import abort


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        CACHE_HOST='localhost',
        CACHE_PORT=6379,
        CACHE_DB=0,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    pp = pprint.PrettyPrinter(indent=4)

    from . import cache
    cache.init_app(app)

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'meep morp'

    @app.route('/add', methods=('POST,'))
    def add():
        return 'nope'

    return app
