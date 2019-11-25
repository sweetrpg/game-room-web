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


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


def create_app(app_name=constants.APPLICATION_NAME):
    app = Flask(app_name)
    app.config.from_object("application.config.BaseConfig")
    # env = DotEnv(app)
    cache.init_app(app)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    from application.blueprints.auth import blueprint as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from application.blueprints.health import blueprint as health_blueprint
    app.register_blueprint(health_blueprint, url_prefix="/health")

    from application.db import db
    db.init_app(app)

    return app
