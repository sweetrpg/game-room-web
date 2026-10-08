# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Tests for the shared header partial's avatar-menu Feedback item and base.html's
feedback-widget asset wiring - see add-anonymous-feedback-reporting (sweetrpg/platform).
"""

import os

import pytest
from flask import Flask

from sweetrpg_game_room_web.application.i18n import init_app as init_i18n

TEMPLATE_DIR = os.path.join(
    os.path.dirname(__file__), "..", "src", "sweetrpg_game_room_web", "application", "templates"
)


@pytest.fixture
def app():
    app = Flask(__name__, template_folder=TEMPLATE_DIR)
    app.config["SECRET_KEY"] = "test"
    init_i18n(app)
    return app


def render_header(app, user):
    with app.test_request_context("/library/"):
        return app.jinja_env.get_template("partials/header.html").render(
            shared_url="http://localhost:8081",
            base_path="",
            user=user,
        )


def test_feedback_item_renders_for_logged_in_user(app):
    html = render_header(app, user={"id": "u1", "name": "Alex", "is_admin": False})

    assert 'id="feedback-trigger"' in html
    assert ">Feedback...<" in html
    # Positioned directly above the logout divider, below any admin link - not the
    # standalone floating-button variant the widget would otherwise inject.
    assert html.index('id="feedback-trigger"') < html.index("Log out")


def test_feedback_item_renders_for_anonymous_user(app):
    html = render_header(app, user={})

    assert 'id="feedback-trigger"' in html
    assert html.index('id="feedback-trigger"') < html.index("Log in")


def test_feedback_item_appears_once_regardless_of_admin_status(app):
    html = render_header(app, user={"id": "u1", "name": "Alex", "is_admin": True})

    assert html.count('id="feedback-trigger"') == 1
    assert "Administration" in html


def test_base_html_wires_feedback_widget_assets():
    with open(os.path.join(TEMPLATE_DIR, "base.html")) as f:
        base_html = f.read()

    assert "feedback-widget.css" in base_html
    assert "feedback-widget.js" in base_html
    assert 'data-api-url="{{ feedback_api_url }}"' in base_html
    assert 'data-trigger-selector="#feedback-trigger"' in base_html
