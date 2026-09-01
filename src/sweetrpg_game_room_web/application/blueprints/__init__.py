# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Main blueprint.
"""

import datetime
import html
import os

import jinja2
import json
import requests
from flask import Blueprint, request, render_template, session, jsonify, current_app, redirect, url_for
from flask_babel import gettext as _
from sweetrpg_game_room_web import __version__
from sweetrpg_game_room_web.application import constants, shared_session
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
        window_parts.append(f"{_('Started:')} {html.escape(mode.starts_at)}")
    if mode.ends_at:
        window_parts.append(f"{_('Expected back:')} {html.escape(mode.ends_at)}")
    window = " &middot; ".join(window_parts)

    body = MAINTENANCE_PAGE_TEMPLATE.format(
        label=html.escape(mode.label or _("Down for maintenance")),
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


def _load_build_info():
    try:
        with open(current_app.config["BUILD_INFO_PATH"]) as f:
            info = json.load(f)
            return info.get("date", "unknown"), info.get("sha", "unknown")[:8]
    except Exception:
        return "unknown", "unknown"


def render_page(page, context={}):

    show_cookie_message = True
    if request.cookies.get("cookies-accepted"):
        show_cookie_message = False

    build_timestamp, build_hash = _load_build_info()
    context.update({"showCookieMessage": show_cookie_message})
    context.setdefault("shared_url", os.environ.get(constants.SHARED_URL, "http://localhost:8081"))
    context.setdefault("catalog_url", os.environ.get(constants.CATALOG_WEB_URL, "http://localhost:8080/catalog"))
    context.setdefault("version", __version__)
    context.setdefault("build_timestamp", build_timestamp)
    context.setdefault("build_hash", build_hash)

    return render_template(page, **context)


def local_redirect(endpoint, **values):
    """Redirect to an in-app endpoint, prefixed with `base_path`.

    `url_for` alone produces an unprefixed path - Traefik strips `base_path` before the request
    reaches this app (see `docs/deployment-conventions.md`'s shared-host Ingress convention), so
    the app's internal route table is unprefixed too. That's correct for routing but wrong for a
    `Location` header, which the browser resolves against the external, prefixed URL - the same
    reason templates manually prepend `{{ base_path }}` to every in-app link.
    """
    base_path = os.environ.get(constants.APPLICATION_BASE_PATH, "")
    return redirect(f"{base_path}{url_for(endpoint, **values)}")


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
    user = shared_session.current_user()
    session[constants.SESSION_ACCESS_TOKEN] = user.get("accessToken") if user else None
    session[constants.SESSION_EMAIL] = user.get("email") if user else None
    session[constants.SESSION_USER_ID] = (
        (_resolve_canonical_user_id(user.get("accessToken")) or user.get("sub")) if user else None
    )
    session[constants.SESSION_NAME] = user.get("name") if user else None
    session[constants.SESSION_ROLES] = user.get("roles") if user else None


def _resolve_canonical_user_id(access_token):
    """Resolve the canonical `users._id` UUID (not the Auth0 subject) via users-api's profile
    endpoint, so every game-room-api `user_id` param is the canonical ID. Returns None when the
    profile is unresolvable so the caller falls back to the subject (anonymous/unprovisioned)."""
    base_url = current_app.config.get(constants.USERS_API_URL)
    if not access_token or not base_url:
        return None
    try:
        resp = requests.get(
            f"{base_url.rstrip('/')}/profile",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=5,
        )
        if resp.status_code != 200:
            return None
        return resp.json().get("user_id")
    except Exception:
        current_app.logger.warning("Unable to resolve canonical user id from users-api profile", exc_info=True)
        return None


@blueprint.errorhandler(Exception)
def error_handler(ex):
    current_app.logger.exception(f"Exception caught: {ex}")
    response = jsonify(message=str(ex))
    response.status_code = ex.code if isinstance(ex, HTTPException) else 500
    return response


def _format_date(iso_string):
    if not iso_string:
        return None
    try:
        return datetime.datetime.fromisoformat(iso_string).strftime("%b %-d, %Y")
    except ValueError:
        return None


def _recent_entries(entries, date_key, limit=3):
    dated = [e for e in entries if e.get(date_key)]
    return sorted(dated, key=lambda e: e[date_key], reverse=True)[:limit]


def _wishlist_entries(wishlists):
    """Flatten every wishlist's entries into a single list for landing-card aggregation."""
    return [e for wl in wishlists for e in (wl.get("entries") or [])]


@blueprint.route("/")
def main_page():
    context = get_context()
    context.update({'appname': "Game Room"})

    user_id = context["user"]["id"]
    if user_id:
        client = current_app.config[constants.GAME_ROOM_CLIENT_KEY]

        library, wishlist_entries, tables = None, [], []
        try:
            library = client.get_library(user_id)
        except Exception:
            current_app.logger.exception("Unable to load library for landing page (user %s)", user_id)
        try:
            wishlists = client.list_wishlists(user_id) or []
            wishlist_entries = _wishlist_entries(wishlists)
        except Exception:
            current_app.logger.exception("Unable to load wishlists for landing page (user %s)", user_id)
        try:
            tables = client.list_tables(user_id) or []
        except Exception:
            current_app.logger.exception("Unable to load tables for landing page (user %s)", user_id)

        library_entries = (library or {}).get("entries") or []

        context.update({
            'library_count': len(library_entries),
            'library_recent': [
                {**e, 'added_at_label': _format_date(e.get('added_at'))}
                for e in _recent_entries(library_entries, 'added_at')
            ],
            'wishlist_count': len(wishlist_entries),
            'wishlist_recent': [
                {**e, 'added_at_label': _format_date(e.get('added_at'))}
                for e in _recent_entries(wishlist_entries, 'added_at')
            ],
            'tables_count': len(tables),
            'tables_recent': [
                {**t, 'updated_at_label': _format_date(t.get('updated_at'))}
                for t in _recent_entries(tables, 'updated_at')
            ],
        })

    return render_page("apps/game-room/index.html", context=context)
