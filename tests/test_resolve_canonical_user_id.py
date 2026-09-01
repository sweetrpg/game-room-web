# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Tests for blueprints._resolve_canonical_user_id.
"""

from unittest.mock import patch, MagicMock

from flask import Flask

from sweetrpg_game_room_web.application import constants
from sweetrpg_game_room_web.application.blueprints import _resolve_canonical_user_id


def _app():
    app = Flask(__name__)
    app.config[constants.USERS_API_URL] = "http://users-api.local"
    return app


@patch("sweetrpg_game_room_web.application.blueprints.requests.get")
def test_calls_profile_endpoint_and_returns_canonical_id(mock_get):
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"user_id": "b3384f5d-78c1-4965-8112-37395c2b8ef3"}
    mock_get.return_value = resp

    with _app().app_context():
        result = _resolve_canonical_user_id("tok-abc")

    assert result == "b3384f5d-78c1-4965-8112-37395c2b8ef3"
    args, kwargs = mock_get.call_args
    assert args[0] == "http://users-api.local/profile"
    assert kwargs["headers"] == {"Authorization": "Bearer tok-abc"}


@patch("sweetrpg_game_room_web.application.blueprints.requests.get")
def test_non_200_returns_none(mock_get):
    resp = MagicMock()
    resp.status_code = 404
    mock_get.return_value = resp

    with _app().app_context():
        assert _resolve_canonical_user_id("tok-abc") is None


def test_no_token_or_base_url_returns_none():
    with _app().app_context():
        assert _resolve_canonical_user_id(None) is None

    app = Flask(__name__)
    with app.app_context():
        assert _resolve_canonical_user_id("tok-abc") is None
