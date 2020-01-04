__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
auth
- Authentication and authorization common endpoints.
"""


from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, current_app, redirect, session, url_for
from werkzeug.exceptions import HTTPException
from urllib.parse import urlencode
import jwt
from application.utils.oauth import auth0, kanka
from application.models.user import User
from application import constants
import os
from application.models.user import User
from application.db import db
from application.cache import cache


AUTH0_CALLBACK_URL = os.environ[constants.AUTH0_CALLBACK_URL]
AUTH0_AUDIENCE = os.environ.get(constants.AUTH0_AUDIENCE)
AUTH0_CLIENT_ID = os.environ[constants.AUTH0_CLIENT_ID]


blueprint = Blueprint("auth", __name__)


# @blueprint.errorhandler(Exception)
# def handle_auth_error(ex):
#     response = jsonify(message=str(ex))
#     response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
#     return response


@blueprint.route('/login')
def login():
    current_app.logger.info(f"/login: {request}")

    print(AUTH0_CALLBACK_URL, AUTH0_AUDIENCE)
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


@blueprint.route('/logout')
def logout():
    current_app.logger.info(f"/logout: {request}")

    session.clear()
    cache.clear()
    params = {
        'returnTo': url_for('home.main_page', _external=True),
        'client_id': AUTH0_CLIENT_ID
        }
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@blueprint.route('/integrate/<service>')
def integrate(service: str):
    current_app.logger.info(f"/logout: {request}")

    # TODO

    return jsonify({}), 204


from . import auth0, kanka
