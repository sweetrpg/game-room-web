# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""catalog_client.py

Thin HTTP client for catalog-api's read endpoints, called server-to-server (no browser-side CORS
concern) - matches every other cross-service call in this codebase (see game_room_client.py).
"""

import requests


class CatalogClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def search_volumes(self, query: str, limit: int = 10):
        """Find volumes whose title exactly matches `query`.

        catalog-api's generic `filter[...]` query param only supports $eq (see api-core.go's
        ConvertQueryParams) - no substring/fuzzy match yet, so this only returns exact-title
        hits. ponytail: exact-match only; add substring search in catalog-api before this can
        return partial matches.
        """
        resp = requests.get(
            f"{self.base_url}/volumes",
            params={"filter[title]": query, "page[limit]": limit},
            timeout=5,
        )
        resp.raise_for_status()
        body = resp.json()
        return [
            {"id": item["id"], "title": item.get("attributes", {}).get("title", item["id"])}
            for item in body.get("data", [])
        ]
