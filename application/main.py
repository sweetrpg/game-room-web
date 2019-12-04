__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
main.py
- creates a Flask app instance and registers the database object
"""


from flask import Flask, session
from flask_session import Session
from flask_cors import CORS
from flask_vue import Vue
from dotenv import load_dotenv, find_dotenv
from application.cache import cache
from application import constants
from logging.config import dictConfig
from application.blueprints import error_page
from werkzeug.exceptions import HTTPException
from redis.client import Redis


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


def create_app(app_name=constants.APPLICATION_NAME):
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s %(module)s: %(message)s',
            }
        },
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

    app = Flask(app_name)
    app.config.from_object("application.config.BaseConfig")
    # env = DotEnv(app)
    cache.init_app(app)

    session = Session(app)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    from application.blueprints.main.home import blueprint as home_blueprint
    app.register_blueprint(home_blueprint, url_prefix="/")

    from application.blueprints.api import blueprint as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    from application.blueprints.apps import blueprint as apps_blueprint
    app.register_blueprint(apps_blueprint, url_prefix="/apps")

    from application.blueprints.account import blueprint as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix="/account")

    from application.blueprints.auth import blueprint as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from application.blueprints.main.health import blueprint as health_blueprint
    app.register_blueprint(health_blueprint, url_prefix="/health")

    from application.db import db
    from flask_migrate import Migrate
    db.init_app(app)
    migrate = Migrate(app, db)

    vue = Vue(app)

    print(app.url_map)

    return app
