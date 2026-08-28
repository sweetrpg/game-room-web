# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""shared_session.py

Read-only access to the suite-wide login session `auth-web` writes under the `sweetrpg_session`
cookie into its own Redis instance. Every other frontend reads this directly rather than relying
on a Traefik ForwardAuth middleware (none exists on this platform).
"""

import datetime
import json

import redis
from flask import current_app, request

SESSION_COOKIE_NAME = "sweetrpg_session"


def _client() -> redis.Redis | None:
    host = current_app.config.get("SHARED_SESSION_REDIS_HOST")
    if not host:
        return None
    return redis.Redis(
        host=host,
        port=current_app.config["SHARED_SESSION_REDIS_PORT"],
        db=current_app.config["SHARED_SESSION_REDIS_DB"],
        password=current_app.config.get("SHARED_SESSION_REDIS_PASSWORD") or None,
        decode_responses=True,
    )


def current_user() -> dict | None:
    """Return the shared session's user dict (sub, name, email, roles, expiry) if the visitor
    has a valid, unexpired session; None otherwise."""
    client = _client()
    if client is None:
        return None
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if not session_id:
        return None
    try:
        raw = client.get(f"vrs-{session_id}")
        if raw is None:
            return None
        session_data = json.loads(raw)
        user = json.loads(session_data["user"])
        expiry = datetime.datetime.fromisoformat(user["expiry"])
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=datetime.timezone.utc)
        if expiry <= datetime.datetime.now(datetime.timezone.utc):
            return None
        return user
    except Exception:
        current_app.logger.warning("shared_session.current_user failed", exc_info=True)
        return None
