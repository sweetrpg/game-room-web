# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Tests for game_room_client.GameRoomClient.
"""

from unittest.mock import patch, MagicMock

from flask import Flask

from sweetrpg_game_room_web.application import constants
from sweetrpg_game_room_web.application.game_room_client import GameRoomClient


def _response(json_body=None, content=b"{}"):
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json.return_value = json_body if json_body is not None else {}
    resp.content = content
    return resp


@patch("sweetrpg_game_room_web.application.game_room_client.requests.get")
def test_get_library_calls_expected_path(mock_get):
    mock_get.return_value = _response({"id": "lib-1", "entries": []})
    client = GameRoomClient("http://game-room-api.local")

    result = client.get_library("user-1")

    mock_get.assert_called_once_with(
        "http://game-room-api.local/users/user-1/library", timeout=5, headers={}
    )
    assert result == {"id": "lib-1", "entries": []}


@patch("sweetrpg_game_room_web.application.game_room_client.requests.request")
def test_set_library_default_visibility_includes_overrides(mock_request):
    mock_request.return_value = _response()
    client = GameRoomClient("http://game-room-api.local/")

    client.set_library_default_visibility("user-1", "public", overrides={"vol-1": "friends"})

    mock_request.assert_called_once_with(
        "PUT",
        "http://game-room-api.local/users/user-1/library/default-visibility",
        timeout=5,
        headers={},
        json={"visibility": "public", "overrides": {"vol-1": "friends"}},
    )


@patch("sweetrpg_game_room_web.application.game_room_client.requests.request")
def test_request_returns_none_for_empty_response(mock_request):
    mock_request.return_value = _response(content=b"")
    client = GameRoomClient("http://game-room-api.local")

    result = client.remove_library_entry("user-1", "vol-1")

    assert result is None


def test_base_url_trailing_slash_stripped():
    client = GameRoomClient("http://game-room-api.local/")
    assert client.base_url == "http://game-room-api.local"


@patch("sweetrpg_game_room_web.application.game_room_client.requests.get")
def test_forwards_session_access_token_as_bearer(mock_get):
    mock_get.return_value = _response({"entries": []})
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test"
    client = GameRoomClient("http://game-room-api.local")

    with app.test_request_context():
        from flask import session

        session[constants.SESSION_ACCESS_TOKEN] = "test-token"
        client.get_library("user-1")

    mock_get.assert_called_once_with(
        "http://game-room-api.local/users/user-1/library",
        timeout=5,
        headers={"Authorization": "Bearer test-token"},
    )


@patch("sweetrpg_game_room_web.application.game_room_client.requests.get")
def test_no_auth_header_outside_request_context(mock_get):
    mock_get.return_value = _response({"entries": []})
    client = GameRoomClient("http://game-room-api.local")

    client.get_library("user-1")

    mock_get.assert_called_once_with(
        "http://game-room-api.local/users/user-1/library", timeout=5, headers={}
    )


@patch("sweetrpg_game_room_web.application.game_room_client.requests.get")
def test_list_wishlists_calls_expected_path(mock_get):
    mock_get.return_value = _response(
        [{"id": "wl-1", "name": "Holiday", "entries": []}]
    )
    client = GameRoomClient("http://game-room-api.local")

    result = client.list_wishlists("user-1")

    mock_get.assert_called_once_with(
        "http://game-room-api.local/users/user-1/wishlists", timeout=5, headers={}
    )
    assert result == [{"id": "wl-1", "name": "Holiday", "entries": []}]


@patch("sweetrpg_game_room_web.application.game_room_client.requests.get")
def test_get_wishlist_calls_expected_path(mock_get):
    mock_get.return_value = _response({"id": "wl-1", "entries": []})
    client = GameRoomClient("http://game-room-api.local")

    result = client.get_wishlist("user-1", "wl-1")

    mock_get.assert_called_once_with(
        "http://game-room-api.local/users/user-1/wishlists/wl-1", timeout=5, headers={}
    )
    assert result == {"id": "wl-1", "entries": []}


@patch("sweetrpg_game_room_web.application.game_room_client.requests.request")
def test_create_wishlist_posts_name_and_visibility(mock_request):
    mock_request.return_value = _response({"id": "wl-1", "name": "Holiday", "visibility": "private"})
    client = GameRoomClient("http://game-room-api.local")

    result = client.create_wishlist("user-1", "Holiday", "private")

    mock_request.assert_called_once_with(
        "POST",
        "http://game-room-api.local/users/user-1/wishlists",
        timeout=5,
        headers={},
        json={"name": "Holiday", "visibility": "private"},
    )
    assert result["id"] == "wl-1"


@patch("sweetrpg_game_room_web.application.game_room_client.requests.request")
def test_delete_wishlist_calls_expected_path(mock_request):
    mock_request.return_value = _response(content=b"")
    client = GameRoomClient("http://game-room-api.local")

    result = client.delete_wishlist("user-1", "wl-1")

    mock_request.assert_called_once_with(
        "DELETE",
        "http://game-room-api.local/users/user-1/wishlists/wl-1",
        timeout=5,
        headers={},
    )
    assert result is None


@patch("sweetrpg_game_room_web.application.game_room_client.requests.request")
def test_add_wishlist_entry_posts_volume(mock_request):
    mock_request.return_value = _response(content=b"")
    client = GameRoomClient("http://game-room-api.local")

    client.add_wishlist_entry("user-1", "wl-1", "vol-1")

    mock_request.assert_called_once_with(
        "POST",
        "http://game-room-api.local/users/user-1/wishlists/wl-1/entries",
        timeout=5,
        headers={},
        json={"volume_id": "vol-1"},
    )


@patch("sweetrpg_game_room_web.application.game_room_client.requests.request")
def test_remove_wishlist_entry_calls_expected_path(mock_request):
    mock_request.return_value = _response(content=b"")
    client = GameRoomClient("http://game-room-api.local")

    client.remove_wishlist_entry("user-1", "wl-1", "vol-1")

    mock_request.assert_called_once_with(
        "DELETE",
        "http://game-room-api.local/users/user-1/wishlists/wl-1/entries/vol-1",
        timeout=5,
        headers={},
    )


@patch("sweetrpg_game_room_web.application.game_room_client.requests.request")
def test_set_wishlist_visibility_posts_visibility(mock_request):
    mock_request.return_value = _response(content=b"")
    client = GameRoomClient("http://game-room-api.local")

    client.set_wishlist_visibility("user-1", "wl-1", "public")

    mock_request.assert_called_once_with(
        "PUT",
        "http://game-room-api.local/users/user-1/wishlists/wl-1/visibility",
        timeout=5,
        headers={},
        json={"visibility": "public"},
    )
