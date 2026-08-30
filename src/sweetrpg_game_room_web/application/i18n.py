# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
i18n
- Localization support: Flask-Babel setup and per-request locale resolution,
per the `web-frontend-localization` spec (sweetrpg/platform's
openspec/changes/full-localization-web-apps). Error pages additionally accept
an explicit `locale` query parameter - they're rendered server-to-server via
Traefik's errors middleware, so there's no browser session to carry a cookie.
"""

from pathlib import Path

from flask import request
from flask_babel import Babel

# Flask-Babel's default translation directory is `<app.root_path>/translations`, and
# app.root_path is unreliable here (see main.py's TEMPLATE_DIR comment - Flask is constructed
# with a plain app_name string, not this module's __name__, so it can't infer root_path and
# falls back to the process's cwd). Resolve the same way TEMPLATE_DIR does: relative to this
# file, independent of cwd.
TRANSLATIONS_DIR = str(Path(__file__).resolve().parent.parent.parent / "translations")

DEFAULT_LOCALE = "en"
LOCALE_COOKIE_NAME = "locale"
LOCALE_QUERY_PARAM = "locale"

# Locales this app can actually render. New locales land as a new
# translations/<code>/LC_MESSAGES catalog plus an entry here.
SUPPORTED_LOCALES = [DEFAULT_LOCALE]


def _resolve_locale():
    """Resolves the request locale: query parameter (error pages), then cookie
    override, then Accept-Language, then English."""
    query_locale = request.args.get(LOCALE_QUERY_PARAM)
    if query_locale and query_locale in SUPPORTED_LOCALES:
        return query_locale

    cookie_locale = request.cookies.get(LOCALE_COOKIE_NAME)
    if cookie_locale and cookie_locale in SUPPORTED_LOCALES:
        return cookie_locale

    return request.accept_languages.best_match(SUPPORTED_LOCALES) or DEFAULT_LOCALE


babel = Babel(locale_selector=_resolve_locale)


def init_app(app):
    app.config.setdefault("BABEL_TRANSLATION_DIRECTORIES", TRANSLATIONS_DIR)
    babel.init_app(app)