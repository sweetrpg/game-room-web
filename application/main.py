__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
main.py
- creates a Flask app instance and registers the database object
"""


from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from application.cache import cache
from application import constants
from logging.config import dictConfig


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

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    from application.blueprints.home import blueprint as home_blueprint
    app.register_blueprint(home_blueprint, url_prefix="/")

    from application.blueprints.apps import blueprint as apps_blueprint
    app.register_blueprint(apps_blueprint, url_prefix="/apps")

    from application.blueprints.profile import blueprint as profile_blueprint
    app.register_blueprint(profile_blueprint, url_prefix="/profile")

    from application.blueprints.auth import blueprint as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from application.blueprints.health import blueprint as health_blueprint
    app.register_blueprint(health_blueprint, url_prefix="/health")

    from application.db import db
    db.init_app(app)

    return app
