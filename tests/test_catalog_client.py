# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Tests for catalog_client.CatalogClient.
"""

from unittest.mock import patch, MagicMock

from sweetrpg_game_room_web.application.catalog_client import CatalogClient


def _response(json_body):
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json.return_value = json_body
    return resp


@patch("sweetrpg_game_room_web.application.catalog_client.requests.get")
def test_search_volumes_calls_search_endpoint(mock_get):
    mock_get.return_value = _response(
        {"data": [{"id": "vol-1", "attributes": {"title": "Curse of Strahd"}}]}
    )
    client = CatalogClient("http://catalog-api.local/")

    result = client.search_volumes("strahd")

    mock_get.assert_called_once_with(
        "http://catalog-api.local/volumes/search",
        params={"q": "strahd"},
        timeout=10,
    )
    assert result == [{"id": "vol-1", "title": "Curse of Strahd"}]


@patch("sweetrpg_game_room_web.application.catalog_client.requests.get")
def test_search_volumes_no_matches_returns_empty_list(mock_get):
    mock_get.return_value = _response({"data": []})
    client = CatalogClient("http://catalog-api.local")

    assert client.search_volumes("nonexistent") == []


@patch("sweetrpg_game_room_web.application.catalog_client.requests.get")
def test_search_volumes_respects_limit(mock_get):
    mock_get.return_value = _response(
        {
            "data": [
                {"id": f"vol-{i}", "attributes": {"title": f"Volume {i}"}}
                for i in range(5)
            ]
        }
    )
    client = CatalogClient("http://catalog-api.local")

    result = client.search_volumes("Volume", limit=2)

    assert len(result) == 2


@patch("sweetrpg_game_room_web.application.catalog_client.requests.get")
def test_get_volume_returns_title(mock_get):
    mock_get.return_value = _response(
        {"data": {"id": "vol-1", "attributes": {"title": "Curse of Strahd"}}}
    )
    client = CatalogClient("http://catalog-api.local/")

    assert client.get_volume("vol-1") == {"id": "vol-1", "title": "Curse of Strahd"}
    mock_get.assert_called_once_with("http://catalog-api.local/volumes/vol-1", timeout=10)


@patch("sweetrpg_game_room_web.application.catalog_client.requests.get")
def test_get_volume_falls_back_to_id_when_untitled(mock_get):
    mock_get.return_value = _response({"data": {"id": "vol-1", "attributes": {}}})
    client = CatalogClient("http://catalog-api.local")

    assert client.get_volume("vol-1") == {"id": "vol-1", "title": "vol-1"}


@patch("sweetrpg_game_room_web.application.catalog_client.CatalogClient.get_volume")
def test_titles_for_maps_ids_and_tolerates_failures(mock_get_volume):
    def side_effect(volume_id):
        if volume_id == "bad":
            raise RuntimeError("catalog down")
        return {"id": volume_id, "title": f"Title {volume_id}"}

    mock_get_volume.side_effect = side_effect
    client = CatalogClient("http://catalog-api.local")

    assert client.titles_for(["a", "bad", "a"]) == {
        "a": "Title a",
        "bad": "bad",
    }
    assert mock_get_volume.call_count == 2
