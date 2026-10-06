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
        """Find volumes whose title, description, or tags contain `query` (case-insensitive).

        catalog-api never shipped a standalone `/volumes/search` route - that work landed on a
        branch that was superseded before merging. The multi-field search this method needs is
        a `filter[q]` query-pushdown param on the regular list endpoint instead (see
        catalog-data.go's `QueryVolumes`/`extractSearchTerm`).
        """
        resp = requests.get(
            f"{self.base_url}/volumes",
            params={"filter[q]": query, "page[limit]": limit},
            timeout=10,
        )
        resp.raise_for_status()
        body = resp.json()
        matches = []
        for item in body.get("data", []):
            title = item.get("attributes", {}).get("title", "")
            matches.append({"id": item["id"], "title": title or item["id"]})
        return matches
