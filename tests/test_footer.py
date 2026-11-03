# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Tests for the standard three-line site footer."""

import datetime
import os
import re

import pytest
from flask import Flask

from sweetrpg_game_room_web.application.blueprints import render_page
from sweetrpg_game_room_web.application.i18n import init_app as init_i18n

TEMPLATE_DIR = os.path.join(
    os.path.dirname(__file__), "..", "src", "sweetrpg_game_room_web", "application", "templates"
)


@pytest.fixture
def app():
    app = Flask(__name__, template_folder=TEMPLATE_DIR)
    app.config["SECRET_KEY"] = "test"
    app.config["BUILD_INFO_PATH"] = "/nonexistent"
    init_i18n(app)
    return app


def _footer(app, monkeypatch, main_url="", base_path=""):
    monkeypatch.setenv("MAIN_URL", main_url)
    monkeypatch.setenv("APPLICATION_BASE_PATH", base_path)
    with app.test_request_context("/"):
        html = render_page("partials/footer.html", {"base_path": base_path})
    lines = re.findall(r'<span class="(footer-line[^"]*)">(.*?)</span>', html, re.S)
    return html, lines


def test_footer_has_three_lines_in_order(app, monkeypatch):
    _, lines = _footer(app, monkeypatch)

    assert len(lines) == 3
    assert f"&copy; {datetime.datetime.now(datetime.timezone.utc).year} Pilgrimage Software" in lines[0][1]
    assert [t for t in ("Terms of Service", "Privacy Policy", "Support") if t in lines[1][1]] == [
        "Terms of Service",
        "Privacy Policy",
        "Support",
    ]
    assert re.search(r"v\S+ &middot; built \S+ / \S+", lines[2][1])


def test_last_line_is_build_line(app, monkeypatch):
    _, lines = _footer(app, monkeypatch)

    assert lines[2][0] == "footer-line footer-build"


@pytest.mark.parametrize("main_url,expected", [("", "/terms"), ("https://dev.sweetrpg.com", "https://dev.sweetrpg.com/terms")])
def test_terms_link_is_site_root(app, monkeypatch, main_url, expected):
    html, _ = _footer(app, monkeypatch, main_url=main_url)

    assert f'<a href="{expected}">Terms of Service</a>' in html


def test_terms_link_is_not_prefixed_under_app_base_path(app, monkeypatch):
    html, _ = _footer(app, monkeypatch, base_path="/game-room")

    assert 'href="/terms"' in html
    assert "/game-room/terms" not in html
