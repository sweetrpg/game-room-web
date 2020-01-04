__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
auth0.py
- Auth0 callback endpoint.
"""


from flask import Blueprint, jsonify, request, current_app, redirect, session, url_for
from application.blueprints.auth import blueprint
from application.utils.oauth import auth0
from application.utils.user import create_or_add_user
from application import constants


@blueprint.route('/auth0/callback')
def auth0_callback_handler():
    current_app.logger.info(f"/auth0/callback: {request}")
    print(request.args)

    token = auth0.authorize_access_token()
    print(f"token: {token}")
    resp = auth0.get('userinfo')
    print(f"resp: {resp}")
    userinfo = resp.json()
    print(f"userinfo: {userinfo}")

    user, identity = create_or_add_user(userinfo)
    print(f"user: {user}, identity: {identity}")

    session[constants.JWT_PAYLOAD] = userinfo
    session[constants.PROFILE_KEY] = {
        'user_id': user.id,
        'name': user.name,
        'picture': user.avatar_url,
    }
    session[constants.CURRENT_USER_ID] = user.id

    # TODO: find redirect url and use that, if present
    return redirect('/account')
