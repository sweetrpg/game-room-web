# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Main blueprint.
"""

import datetime
import html
import os

import analytics
import jinja2
from flask import Blueprint, request, render_template, session, jsonify, current_app
from sweetrpg_game_room_web.application import constants
from sweetrpg_game_room_web.application import shared_session
from sweetrpg_web_core.helpers.context import get_context
from werkzeug.exceptions import HTTPException

MAINTENANCE_SCOPES = ["platform", "service:game-room"]

# Health check routes must stay reachable during maintenance so orchestration
# doesn't mark the pod unhealthy and restart it.
HEALTH_PATH_PREFIX = "/health"

MAINTENANCE_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Game Room - Maintenance</title>
<style>
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #1b1d23;
    color: #f4f4f5;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    margin: 0;
  }}
  .card {{
    max-width: 32rem;
    padding: 2.5rem;
    background: #24262e;
    border-radius: 0.75rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
  }}
  h1 {{
    margin-top: 0;
    font-size: 1.5rem;
  }}
  p {{
    line-height: 1.5;
    color: #c7c9d1;
  }}
  .window {{
    margin-top: 1.5rem;
    font-size: 0.875rem;
    color: #9195a1;
  }}
</style>
</head>
<body>
<div class="card">
  <h1>{label}</h1>
  <p>{description}</p>
  <div class="window">{window}</div>
</div>
</body>
</html>
"""


def render_maintenance_page(mode):
    window_parts = []
    if mode.starts_at:
        window_parts.append(f"Started: {html.escape(mode.starts_at)}")
    if mode.ends_at:
        window_parts.append(f"Expected back: {html.escape(mode.ends_at)}")
    window = " &middot; ".join(window_parts)

    body = MAINTENANCE_PAGE_TEMPLATE.format(
        label=html.escape(mode.label or "Down for maintenance"),
        description=html.escape(mode.description or ""),
        window=window,
    )
    return body, 503


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
    context.setdefault("shared_url", os.environ.get(constants.SHARED_URL, "http://localhost:8081"))
    print(f"context: {context}")

    return render_template(page, **context)


class UserAuthorizationException(Exception):
    def __init__(self, reason: str):
        self.reason = reason


blueprint = Blueprint("web", __name__)


@blueprint.before_request
def _check_maintenance_mode():
    if request.path.startswith(HEALTH_PATH_PREFIX):
        return None

    admin_client = current_app.config.get(constants.ADMIN_API_CLIENT_KEY)
    if admin_client is None:
        return None

    modes = admin_client.fetch_maintenance_modes(MAINTENANCE_SCOPES)
    if modes:
        return render_maintenance_page(modes[0])

    return None


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

    # Read the suite-wide login session directly (see shared_session.py) rather than trusting
    # X-Forwarded-* headers from an upstream auth proxy - no such proxy has ever been wired up
    # in front of this app, so those headers were always empty and every authenticated write to
    # shelf-api (add/remove entries, set visibility, create/update/delete a table) 403'd
    # unconditionally.
    user = shared_session.current_user()
    session[constants.SESSION_ACCESS_TOKEN] = user.get("accessToken") if user else None
    session[constants.SESSION_EMAIL] = user.get("email") if user else None
    session[constants.SESSION_USER_ID] = user.get("sub") if user else None

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
        'appname': "Game Room",
    })

    print(f"context: {context}")
    return render_page("apps/game-room/index.html", context=context)

# from sweetrpg_game_room_web.application.blueprints import authors
