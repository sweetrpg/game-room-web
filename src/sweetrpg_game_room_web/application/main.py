# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""main.py

Creates a Flask app instance and registers various services and middleware.
"""

from flask import Flask, session, g
from flask_cors import CORS
from flask_session import Session
from dotenv import load_dotenv, find_dotenv
from sweetrpg_game_room_web.application.cache import cache
from sweetrpg_game_room_web.application import constants
from sweetrpg_client.client import Client as APIClient
from sweetrpg_admin_api_client import AdminClient
from sweetrpg_game_room_web.application.game_room_client import GameRoomClient
from sweetrpg_game_room_web.application.catalog_client import CatalogClient
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
            },
            "handlers": {"wsgi": {"class": "logging.StreamHandler", "stream": "ext://flask.logging.wsgi_errors_stream", "formatter": "default"}},
            "root": {"level": os.environ.get(constants.LOG_LEVEL) or "INFO", "handlers": ["wsgi"]},
        }
    )

    app = Flask(__name__)
    app.debug = app.config["DEBUG"]
    app.config.from_object("sweetrpg_game_room_web.application.config.BaseConfig")
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

    # from sweetrpg_game_room_web.application.blueprints import api
    # from sweetrpg_game_room_web.application.auth import oauth
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

    app.logger.info("Setting up API client...")
    app.config[constants.SWEETRPG_API_CLIENT_KEY] = APIClient(os.environ[constants.GAME_ROOM_API_BASE_URL])

    app.logger.info("Setting up admin-api client...")
    app.config[constants.ADMIN_API_CLIENT_KEY] = AdminClient(base_url=app.config.get(constants.ADMIN_API_URL))

    app.logger.info("Setting up game room client...")
    app.config[constants.GAME_ROOM_CLIENT_KEY] = GameRoomClient(os.environ[constants.GAME_ROOM_API_BASE_URL])

    app.logger.info("Setting up catalog client...")
    app.config[constants.CATALOG_CLIENT_KEY] = CatalogClient(app.config.get(constants.CATALOG_API_URL) or "")

    app.logger.info("Setting up endpoints...")

    from sweetrpg_game_room_web.application.blueprints import blueprint as main_blueprint

    from sweetrpg_game_room_web.application.blueprints.licenses import blueprint as licenses_blueprint
    main_blueprint.register_blueprint(licenses_blueprint)
    from sweetrpg_game_room_web.application.blueprints.volumes import blueprint as volumes_blueprint
    main_blueprint.register_blueprint(volumes_blueprint)
    from sweetrpg_game_room_web.application.blueprints.persons import blueprint as persons_blueprint
    main_blueprint.register_blueprint(persons_blueprint)

    from sweetrpg_game_room_web.application.blueprints.library import blueprint as library_blueprint
    main_blueprint.register_blueprint(library_blueprint)
    from sweetrpg_game_room_web.application.blueprints.wishlist import blueprint as wishlist_blueprint
    main_blueprint.register_blueprint(wishlist_blueprint)
    from sweetrpg_game_room_web.application.blueprints.tables import blueprint as tables_blueprint
    main_blueprint.register_blueprint(tables_blueprint)

    from sweetrpg_web_core.blueprints.health import blueprint as health_blueprint
    main_blueprint.register_blueprint(health_blueprint)

    # from application.blueprints.billing import blueprint as billing_blueprint
    # app.register_blueprint(billing_blueprint, url_prefix="/billing")

    app.register_blueprint(main_blueprint)  # , url_prefix=f"/{os.environ[constants.APPLICATION_BASE_PATH]}")

    # vue = Vue(app)

    # app.wsgi_app = SassMiddleware(app.wsgi_app, {
    #     'application': ('static/sass', 'static/css', '/static/css')
    # })
    # scss = Scss(app, static_dir='static', asset_dir='assets')

    print(app.url_map)

    return app
