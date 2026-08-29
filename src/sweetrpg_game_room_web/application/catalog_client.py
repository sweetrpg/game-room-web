# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""catalog_client.py

Thin HTTP client for catalog-api's read endpoints, called server-to-server (no browser-side CORS
concern) - matches every other cross-service call in this codebase (see game_room_client.py).
"""

import requests

# catalog-api has a dedicated `/<entity>/search?q=...` endpoint (data.SearchPublishers,
# SearchLicenses, SearchPersons, SearchStudios, SearchSystems) for every entity except volumes -
# no data.SearchVolumes exists yet. ponytail: substring-match client-side over the first
# PAGE_SIZE volumes instead of a real server-side search; add /volumes/search (mirroring the
# other entities) in catalog-api + catalog-data.go, then swap this for a single filtered call.
_SEARCH_PAGE_SIZE = 200


class CatalogClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def search_volumes(self, query: str, limit: int = 10):
        """Find volumes whose title contains `query` (case-insensitive)."""
        resp = requests.get(
            f"{self.base_url}/volumes",
            params={"page[limit]": _SEARCH_PAGE_SIZE},
            timeout=5,
        )
        resp.raise_for_status()
        body = resp.json()
        query_lower = query.lower()
        matches = []
        for item in body.get("data", []):
            title = item.get("attributes", {}).get("title", "")
            if query_lower in title.lower():
                matches.append({"id": item["id"], "title": title or item["id"]})
                if len(matches) >= limit:
                    break
        return matches
