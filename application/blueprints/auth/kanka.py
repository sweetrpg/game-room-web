__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
kanka.py
- Kanka callback endpoint.
"""


from flask import Blueprint, jsonify, request, current_app, redirect, session, url_for
from application.blueprints.auth import blueprint
from application.utils.oauth import kanka
from application.utils.user import create_or_add_user


@blueprint.route('/kanka/callback')
def kanka_callback_handler():
    current_app.logger.info(f"/kanka/callback: {request}")
    print(request.args)

    token = kanka.authorize_access_token()
    print(f"token: {token}")
    resp = kanka.get('userinfo')
    print(f"resp: {resp}")
    userinfo = resp.json()
    print(f"userinfo: {userinfo}")

    # TODO: what do we do here? create an identity? store token for API calls? setup an integration?
    # user, identity = create_or_add_user(userinfo)
    # print(f"user: {user}, identity: {identity}")

    # TODO: find redirect url and use that, if present
    return redirect('/account')
