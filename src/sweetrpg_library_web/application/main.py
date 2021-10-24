# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""main.py

Creates a Flask app instance and registers various services and middleware.
"""

from flask import Flask, session
from flask_cors import CORS
from flask_migrate import Migrate
from flask_session import Session
from dotenv import load_dotenv, find_dotenv
from sweetrpg_library_web.application.cache import cache
from sweetrpg_library_web.application import constants
from sweetrpg_library_web.application.auth import oauth
from logging.config import dictConfig
from redis.client import Redis
from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware
import analytics
import os


ENV_FILE = find_dotenv()
if ENV_FILE:
    print(f"Loading environment from {ENV_FILE}...")
    load_dotenv(ENV_FILE)


def create_app(app_name=constants.APPLICATION_NAME):
    print("Configuring logging...")
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s %(module)s/%(funcName)s: %(message)s",
                },
                "logstash": {
                    "class": "logstash_async.formatter.FlaskLogstashFormatter",
                    "metadata": {"beat": "sweetrpg-library-api"},
                }
            },
            "handlers": {"wsgi": {"class": "logging.StreamHandler", "stream": "ext://flask.logging.wsgi_errors_stream", "formatter": "default"},
                         "logstash": {"class": "logstash_async.handler.AsynchronousLogstashHandler", "formatter": "logstash",
                                      "host": os.environ[constants.LOGSTASH_HOST],
                                      "port": int(os.environ[constants.LOGSTASH_PORT]),
                                      "database_path": "/tmp/sweetrpg_library_web_flask_logstash.db",
                                      "transport": "logstash_async.transport.BeatsTransport",
                                      }},
            "root": {"level": os.environ.get(constants.LOG_LEVEL) or "INFO", "handlers": ["wsgi", "logstash"]},
        }
    )

    app = Flask(app_name)
    app.debug = app.config["DEBUG"]
    app.config.from_object("sweetrpg_library_web.application.config.BaseConfig")
    # env = DotEnv(app)

    app.logger.info("Setting up cache...")
    cache.init_app(app)

    # app.logger.info("Setting up cache...")
    # oauth.init_app(app)

    app.logger.info("Setting up analytics...")
    analytics.write_key = app.config.get("SEGMENT_WRITE_KEY")
    analytics.debug = app.config.get("DEBUG") or False

    app.logger.info("Setting up session manager...")
    session = Session(app)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    if not app.debug:
        app.logger.info("Setting up Sentry...")
        sentry = SentryWsgiMiddleware(app)

    # from sweetrpg_library_web.application.blueprints import api
    # from sweetrpg_library_web.application.auth import oauth
    # from authlib.integrations.flask_client import OAuth
    # api.init_app(app)
    # oauth.init_app(app)
    # oauth.app = app
    # api.oauth_manager(oauth)
    # oauth.scope_setter(get_scope)

    # _oauth = OAuth(app)
    # oauth.register('auth0',
    #                client_id=os.environ[constants.AUTH0_CLIENT_ID],
    #                client_secret=os.environ[constants.AUTH0_CLIENT_SECRET],
    #                api_base_url=os.environ[constants.AUTH0_DOMAIN],
    #                access_token_url=os.environ[constants.AUTH0_CALLBACK_URL],
    #                authorize_url=os.environ[constants.AUTH0_LOGIN_URL],
    #                client_kwargs={
    #                    'scope': 'openid profile email',
    #                })

    app.logger.info("Setting up endpoints...")

    # from sweetrpg_library_web.application.blueprints.volumes import blueprint as volumes_blueprint
    # app.register_blueprint(volumes_blueprint, url_prefix="/volumes")

    # from sweetrpg_library_web.application.blueprints.volumes import setup_routes as setup_volume_routes
    # setup_volume_routes(app)
    #
    # from sweetrpg_library_web.application.blueprints.authors import setup_routes as setup_author_routes
    # setup_author_routes(app)
    #
    # from sweetrpg_library_web.application.blueprints.publishers import setup_routes as setup_publisher_routes
    # setup_publisher_routes(app)
    #
    # from sweetrpg_library_web.application.blueprints.reviews import setup_routes as setup_review_routes
    # setup_review_routes(app)
    #
    # from sweetrpg_library_web.application.blueprints.studios import setup_routes as setup_studio_routes
    # setup_studio_routes(app)
    #
    # from sweetrpg_library_web.application.blueprints.systems import setup_routes as setup_system_routes
    # setup_system_routes(app)
    #
    # from sweetrpg_library_web.application.blueprints.tags import setup_routes as setup_tag_routes
    # setup_tag_routes(app)

    # from application.blueprints.api import blueprint as api_blueprint
    # app.register_blueprint(api_blueprint, url_prefix="/api/v1")
    #
    # from application.blueprints.apps import blueprint as apps_blueprint
    # app.register_blueprint(apps_blueprint, url_prefix="/apps")
    #
    # from application.blueprints.account import blueprint as account_blueprint
    # app.register_blueprint(account_blueprint, url_prefix="/account")
    #
    # from application.blueprints.auth import blueprint as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from sweetrpg_web_core.blueprints.health import blueprint as health_blueprint

    app.register_blueprint(health_blueprint, url_prefix="/health")

    # from application.blueprints.billing import blueprint as billing_blueprint
    # app.register_blueprint(billing_blueprint, url_prefix="/billing")

    # vue = Vue(app)

    # app.wsgi_app = SassMiddleware(app.wsgi_app, {
    #     'application': ('static/sass', 'static/css', '/static/css')
    # })
    # scss = Scss(app, static_dir='static', asset_dir='assets')

    # stripe.api_key = app.config['STRIPE_API_KEY']

    print(app.url_map)

    return app
