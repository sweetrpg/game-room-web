# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""game_room_client.py

Thin HTTP client for game-room-api's library/wishlist/table endpoints. Separate from the legacy
sweetrpg_client.Client (which targets the old Library/Catalog-shaped API) - game-room-api's
domain endpoints don't exist yet under that client's contract. Callers get None on any failure
so game-room-web keeps rendering while game-room-api's data layer (openspec `shelf-service`
task group 2) is still being built.
"""

import requests
from flask import session

from sweetrpg_game_room_web.application import constants


class GameRoomClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def _auth_headers(self):
        try:
            token = session.get(constants.SESSION_ACCESS_TOKEN)
        except RuntimeError:
            # Outside a Flask request context (e.g. direct unit tests) - no session to read.
            return {}
        return {"Authorization": f"Bearer {token}"} if token else {}

    def _get(self, path: str, **kwargs):
        headers = {**self._auth_headers(), **kwargs.pop("headers", {})}
        resp = requests.get(f"{self.base_url}{path}", timeout=5, headers=headers, **kwargs)
        resp.raise_for_status()
        return resp.json()

    def _request(self, method: str, path: str, **kwargs):
        headers = {**self._auth_headers(), **kwargs.pop("headers", {})}
        resp = requests.request(method, f"{self.base_url}{path}", timeout=5, headers=headers, **kwargs)
        resp.raise_for_status()
        if resp.content:
            return resp.json()
        return None

    # -- library --

    def get_library(self, user_id: str):
        return self._get(f"/users/{user_id}/library")

    def add_library_entry(self, user_id: str, volume_id: str, volume_title: str = ""):
        return self._request(
            "POST",
            f"/users/{user_id}/library/entries",
            json={"volume_id": volume_id, "volume_title": volume_title or None},
        )

    def remove_library_entry(self, user_id: str, volume_id: str):
        return self._request("DELETE", f"/users/{user_id}/library/entries/{volume_id}")

    def preview_library_default_visibility(self, user_id: str, visibility: str):
        return self._request(
            "POST", f"/users/{user_id}/library/default-visibility/preview", json={"visibility": visibility}
        )

    def set_library_default_visibility(self, user_id: str, visibility: str, overrides: dict | None = None):
        payload = {"visibility": visibility}
        if overrides:
            payload["overrides"] = overrides
        return self._request("PUT", f"/users/{user_id}/library/default-visibility", json=payload)

    def set_library_entry_visibility(self, user_id: str, volume_id: str, visibility: str | None):
        return self._request(
            "PUT", f"/users/{user_id}/library/entries/{volume_id}/visibility", json={"visibility": visibility}
        )

    # -- wishlist --

    def list_wishlists(self, user_id: str):
        return self._get(f"/users/{user_id}/wishlists")

    def get_wishlist(self, user_id: str, wishlist_id: str):
        return self._get(f"/users/{user_id}/wishlists/{wishlist_id}")

    def create_wishlist(self, user_id: str, name: str, visibility: str = "private"):
        return self._request(
            "POST", f"/users/{user_id}/wishlists", json={"name": name, "visibility": visibility}
        )

    def delete_wishlist(self, user_id: str, wishlist_id: str):
        return self._request("DELETE", f"/users/{user_id}/wishlists/{wishlist_id}")

    def add_wishlist_entry(self, user_id: str, wishlist_id: str, volume_id: str, volume_title: str = ""):
        return self._request(
            "POST",
            f"/users/{user_id}/wishlists/{wishlist_id}/entries",
            json={"volume_id": volume_id, "volume_title": volume_title or None},
        )

    def remove_wishlist_entry(self, user_id: str, wishlist_id: str, volume_id: str):
        return self._request("DELETE", f"/users/{user_id}/wishlists/{wishlist_id}/entries/{volume_id}")

    def set_wishlist_visibility(self, user_id: str, wishlist_id: str, visibility: str):
        return self._request(
            "PUT", f"/users/{user_id}/wishlists/{wishlist_id}/visibility", json={"visibility": visibility}
        )

    # -- tables --

    def list_tables(self, user_id: str):
        return self._get(f"/users/{user_id}/tables")

    def get_table(self, user_id: str, table_id: str):
        return self._get(f"/users/{user_id}/tables/{table_id}")

    def create_table(self, user_id: str, name: str, visibility: str = "private"):
        return self._request(
            "POST", f"/users/{user_id}/tables", json={"name": name, "visibility": visibility}
        )

    def update_table(self, user_id: str, table_id: str, name: str, visibility: str):
        return self._request(
            "PUT", f"/users/{user_id}/tables/{table_id}", json={"name": name, "visibility": visibility}
        )

    def delete_table(self, user_id: str, table_id: str):
        return self._request("DELETE", f"/users/{user_id}/tables/{table_id}")

    def add_table_volume(self, user_id: str, table_id: str, volume_id: str, volume_title: str = ""):
        return self._request(
            "POST",
            f"/users/{user_id}/tables/{table_id}/volumes",
            json={"volume_id": volume_id, "volume_title": volume_title or None},
        )

    def remove_table_volume(self, user_id: str, table_id: str, volume_id: str):
        return self._request("DELETE", f"/users/{user_id}/tables/{table_id}/volumes/{volume_id}")
