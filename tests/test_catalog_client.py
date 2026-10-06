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
def test_search_volumes_uses_filter_q_query_pushdown(mock_get):
    mock_get.return_value = _response(
        {"data": [{"id": "vol-1", "attributes": {"title": "Curse of Strahd"}}]}
    )
    client = CatalogClient("http://catalog-api.local/")

    result = client.search_volumes("strahd")

    mock_get.assert_called_once_with(
        "http://catalog-api.local/volumes",
        params={"filter[q]": "strahd", "page[limit]": 10},
        timeout=10,
    )
    assert result == [{"id": "vol-1", "title": "Curse of Strahd"}]


@patch("sweetrpg_game_room_web.application.catalog_client.requests.get")
def test_search_volumes_no_matches_returns_empty_list(mock_get):
    mock_get.return_value = _response({"data": []})
    client = CatalogClient("http://catalog-api.local")

    assert client.search_volumes("nonexistent") == []


@patch("sweetrpg_game_room_web.application.catalog_client.requests.get")
def test_search_volumes_passes_limit_as_page_limit(mock_get):
    """The limit is enforced server-side via `page[limit]`, not truncated client-side - this
    mock's response already respects it, matching what catalog-api's query-pushdown returns."""
    mock_get.return_value = _response(
        {
            "data": [
                {"id": f"vol-{i}", "attributes": {"title": f"Volume {i}"}}
                for i in range(2)
            ]
        }
    )
    client = CatalogClient("http://catalog-api.local")

    result = client.search_volumes("Volume", limit=2)

    mock_get.assert_called_once_with(
        "http://catalog-api.local/volumes",
        params={"filter[q]": "Volume", "page[limit]": 2},
        timeout=10,
    )
    assert len(result) == 2
