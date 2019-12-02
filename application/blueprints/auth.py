__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
auth.py
- Authentication and authorization endpoints.
"""


from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, current_app, redirect, session, url_for
from werkzeug.exceptions import HTTPException
from urllib.parse import urlencode
import jwt
from application.models.user import User
from application import constants
from application.utils.oauth import auth0
import os
from application.models.user import User
from application.db import db


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
    params = {
        'returnTo': url_for('home.main_page', _external=True),
        'client_id': AUTH0_CLIENT_ID
        }
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@blueprint.route('/callback')
def callback_handling():
    current_app.logger.info(f"/callback: {request}")
    print(request.args)

    token = auth0.authorize_access_token()
    print(f"token: {token}")
    resp = auth0.get('userinfo')
    print(f"resp: {resp}")
    userinfo = resp.json()
    print(f"userinfo: {userinfo}")

    user = User.query.filter_by(email=userinfo['email']).first()
    if not user:
        user = User(identity_id=userinfo['sub'], email=userinfo['email'])
        user.nickname = userinfo['nickname']
        user.name = userinfo['name']
        # https://www.gravatar.com/avatar/#(gravatarHash)?s=30
        user.avatar_url = userinfo['picture']
        db.session.add(user)
        db.session.commit()
    print(user)

    session[constants.JWT_PAYLOAD] = userinfo
    session[constants.PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    session[constants.CURRENT_USER_ID] = user.id
    return redirect('/profile')


# from . import login, register
