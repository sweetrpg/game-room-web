# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Main blueprint.
"""

import datetime

import analytics
import jinja2
from flask import Blueprint, request, render_template, session, jsonify, current_app
from sweetrpg_library_web.application import constants
from sweetrpg_web_core.helpers.context import get_context
from werkzeug.exceptions import HTTPException


def error_page(message, code):
    context = {
        "code": code,
        "message": message,
    }
    try:
        return render_page(f"errors/{code}.html")
    except jinja2.TemplateNotFound:
        return render_page("errors/error.html", context)


def render_page(page, context={}):

    show_cookie_message = True
    if request.cookies.get("cookies-accepted"):
        show_cookie_message = False

    userinfo = session.get(constants.PROFILE_KEY)
    if userinfo:
        context.update(
            {
                "showCookieMessage": show_cookie_message,
                "userinfo": userinfo,
            }
        )
    print(f"context: {context}")

    return render_template(page, **context)


class UserAuthorizationException(Exception):
    def __init__(self, reason: str):
        self.reason = reason


blueprint = Blueprint("web", __name__)


@blueprint.before_request
def _populate():
    print(f"session: {session}")
    print(f"headers: {request.headers}")
    print(f"cookies: {request.cookies}")
    print(f"args: {request.args}")

    userinfo = None
    if constants.PROFILE_KEY in session:
        userinfo = session[constants.PROFILE_KEY]
    elif constants.SWEETRPG_AUTH_KEY in request.cookies:
        userinfo = request.cookies[constants.SWEETRPG_AUTH_KEY]
        session[constants.PROFILE_KEY] = userinfo
    session[constants.SESSION_ACCESS_TOKEN] = request.headers.get('X-Forwarded-Access-Token')
    session[constants.SESSION_EMAIL] = request.headers.get('X-Forwarded-Email')
    session[constants.SESSION_USER_ID] = request.headers.get('X-Forwarded-User')

    print(f"(updated) session: {session}")
    print(f"userinfo: {userinfo}")


@blueprint.before_request
def _track():
    email = session.get(constants.SESSION_EMAIL)
    print(f"email: {email}")
    user_id = session.get(constants.SESSION_USER_ID)
    print(f"user_id: {user_id}")
    if user_id and email:
        analytics.identify(user_id, {
            'email': email,
            'created_at': datetime.datetime.now()
        })

        analytics.track(user_id, request.url, {
            'user_agent': request.headers.get('User-Agent')
        })


@blueprint.errorhandler(Exception)
def error_handler(ex):
    current_app.logger.exception(f"Exception caught: {ex}")
    response = jsonify(message=str(ex))
    response.status_code = ex.code if isinstance(ex, HTTPException) else 500
    return response


@blueprint.route("/")
def main_page():
    context = get_context()
    context.update({
        # 'user_info': session.get(constants.SWEETRPG_SESSION_USER_INFO),
        'appname': "Library",
    })

    print(f"context: {context}")
    return render_page("apps/library/index.html", context=context)

# from sweetrpg_library_web.application.blueprints import authors
