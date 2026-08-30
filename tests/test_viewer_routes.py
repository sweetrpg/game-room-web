# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Tests for viewer-based library/wishlist/table pages: an owner sees edit controls, another
viewer (including anonymous) sees the same data read-only. game-room-api does the actual visibility
filtering (game-room-api#154 task 2.7); this only checks the web layer renders what it's given
without a way to write to someone else's collection.
"""

import os
from unittest.mock import MagicMock

import pytest
from flask import Flask

TEMPLATE_DIR = os.path.join(
    os.path.dirname(__file__), "..", "src", "sweetrpg_game_room_web", "application", "templates"
)


@pytest.fixture
def app():
    app = Flask(__name__, template_folder=TEMPLATE_DIR)
    app.config["SECRET_KEY"] = "test"
    app.config["GAME_ROOM_CLIENT_KEY"] = "game-room-client"
    app.config["GAME_ROOM_CLIENT_KEY"] = MagicMock()

    from sweetrpg_game_room_web.application import constants
    from sweetrpg_game_room_web.application.blueprints.library import blueprint as library_blueprint
    from sweetrpg_game_room_web.application.blueprints.wishlist import blueprint as wishlist_blueprint

    app.register_blueprint(library_blueprint)
    app.config[constants.GAME_ROOM_CLIENT_KEY] = MagicMock(
        get_library=MagicMock(
            return_value={
                "user_id": "user-2",
                "default_visibility": "public",
                "entries": [{"volume_id": "vol-1", "visibility_override": None}],
            }
        ),
        get_wishlist=MagicMock(
            return_value={
                "user_id": "user-2",
                "id": "wl-1",
                "name": "Holiday",
                "visibility": "private",
                "entries": [{"volume_id": "vol-2", "added_at": "2026-08-28T12:00:00+00:00"}],
            }
        ),
    )
    app.register_blueprint(wishlist_blueprint)
    return app


def test_anonymous_viewer_sees_no_owner_controls(app):
    client = app.test_client()
    resp = client.get("/library/users/user-2")

    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "vol-1" in body
    assert 'id="visibility-menu-trigger"' not in body
    assert "Remove" not in body


def test_owner_sees_edit_controls(app):
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["user_id"] = "user-2"

    resp = client.get("/library/users/user-2")

    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert 'id="visibility-menu-trigger"' in body
    assert "Remove" in body


def test_own_library_page_without_login_shows_login_prompt(app):
    client = app.test_client()
    resp = client.get("/library/")
    assert resp.status_code == 200
    assert "Log in to see your library" in resp.get_data(as_text=True)


def test_anonymous_visitor_sees_wishlist_detail_read_only(app):
    client = app.test_client()
    resp = client.get("/wishlist/users/user-2/wl-1")

    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Holiday" in body
    assert 'id="visibility-menu-trigger"' not in body
    assert "Delete wishlist" not in body
    assert "Remove" not in body


def test_owner_sees_wishlist_edit_controls(app):
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["user_id"] = "user-2"

    resp = client.get("/wishlist/users/user-2/wl-1")

    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert 'id="visibility-menu-trigger"' in body
    assert "Delete wishlist" in body
    assert "Remove" in body


def test_own_wishlist_page_without_login_shows_login_prompt(app):
    client = app.test_client()
    resp = client.get("/wishlist/")
    assert resp.status_code == 200
    assert "Log in to see your wishlists." in resp.get_data(as_text=True)
