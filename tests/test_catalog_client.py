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
def test_search_volumes_maps_jsonapi_response(mock_get):
    mock_get.return_value = _response(
        {"data": [{"id": "vol-1", "attributes": {"title": "Curse of Strahd"}}]}
    )
    client = CatalogClient("http://catalog-api.local/")

    result = client.search_volumes("Curse of Strahd")

    mock_get.assert_called_once_with(
        "http://catalog-api.local/volumes",
        params={"filter[title]": "Curse of Strahd", "page[limit]": 10},
        timeout=5,
    )
    assert result == [{"id": "vol-1", "title": "Curse of Strahd"}]


@patch("sweetrpg_game_room_web.application.catalog_client.requests.get")
def test_search_volumes_no_matches_returns_empty_list(mock_get):
    mock_get.return_value = _response({"data": []})
    client = CatalogClient("http://catalog-api.local")

    assert client.search_volumes("nonexistent") == []
