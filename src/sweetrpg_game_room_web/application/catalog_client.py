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
        """Find volumes whose title contains `query` (case-insensitive)."""
        resp = requests.get(
            f"{self.base_url}/volumes/search",
            params={"q": query},
            timeout=10,
        )
        resp.raise_for_status()
        body = resp.json()
        matches = []
        for item in body.get("data", []):
            title = item.get("attributes", {}).get("title", "")
            matches.append({"id": item["id"], "title": title or item["id"]})
            if len(matches) >= limit:
                break
        return matches

    def get_volume(self, volume_id: str):
        """Fetch one volume. Title falls back to the id when the volume has none."""
        resp = requests.get(f"{self.base_url}/volumes/{volume_id}", timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data") or {}
        title = data.get("attributes", {}).get("title", "")
        return {"id": volume_id, "title": title or volume_id}

    def titles_for(self, volume_ids):
        """Map volume ids to titles for display. Any id that doesn't resolve maps to itself,
        so a single missing volume never blanks out the rest of the list."""
        titles = {}
        for volume_id in volume_ids:
            if volume_id in titles:
                continue
            try:
                titles[volume_id] = self.get_volume(volume_id)["title"]
            except Exception:
                titles[volume_id] = volume_id
        return titles
