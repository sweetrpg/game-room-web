# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Tests for shelf_client.ShelfClient.
"""

from unittest.mock import patch, MagicMock

from sweetrpg_game_room_web.application.shelf_client import ShelfClient


def _response(json_body=None, content=b"{}"):
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json.return_value = json_body if json_body is not None else {}
    resp.content = content
    return resp


@patch("sweetrpg_game_room_web.application.shelf_client.requests.get")
def test_get_library_calls_expected_path(mock_get):
    mock_get.return_value = _response({"id": "lib-1", "entries": []})
    client = ShelfClient("http://shelf-api.local")

    result = client.get_library("user-1")

    mock_get.assert_called_once_with(
        "http://shelf-api.local/users/user-1/library", timeout=5, headers={}
    )
    assert result == {"id": "lib-1", "entries": []}


@patch("sweetrpg_game_room_web.application.shelf_client.requests.request")
def test_set_library_default_visibility_includes_overrides(mock_request):
    mock_request.return_value = _response()
    client = ShelfClient("http://shelf-api.local/")

    client.set_library_default_visibility("user-1", "public", overrides={"vol-1": "friends"})

    mock_request.assert_called_once_with(
        "PUT",
        "http://shelf-api.local/users/user-1/library/default-visibility",
        timeout=5,
        headers={},
        json={"visibility": "public", "overrides": {"vol-1": "friends"}},
    )


@patch("sweetrpg_game_room_web.application.shelf_client.requests.get")
def test_get_library_forwards_bearer_token(mock_get):
    mock_get.return_value = _response({"id": "lib-1", "entries": []})
    client = ShelfClient("http://shelf-api.local")

    client.get_library("user-1", access_token="tok-123")

    mock_get.assert_called_once_with(
        "http://shelf-api.local/users/user-1/library",
        timeout=5,
        headers={"Authorization": "Bearer tok-123"},
    )


@patch("sweetrpg_game_room_web.application.shelf_client.requests.request")
def test_request_returns_none_for_empty_response(mock_request):
    mock_request.return_value = _response(content=b"")
    client = ShelfClient("http://shelf-api.local")

    result = client.remove_library_entry("user-1", "vol-1")

    assert result is None


def test_base_url_trailing_slash_stripped():
    client = ShelfClient("http://shelf-api.local/")
    assert client.base_url == "http://shelf-api.local"
