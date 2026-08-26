# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""shelf_client.py

Thin HTTP client for shelf-api's library/wishlist/table endpoints. Separate from the legacy
sweetrpg_client.Client (which targets the old Library/Catalog-shaped API) - shelf-api's domain
endpoints don't exist yet under that client's contract. Callers get None on any failure so
shelf-web keeps rendering while shelf-api's data layer (openspec `shelf-service` task group 2)
is still being built.

Every method accepts an optional `access_token` - the caller's Auth0 access token from the
shared session (see shared_session.py) - forwarded as `Authorization: Bearer <token>`.
game-room-api's `authz.RequireOwner` middleware rejects every write (add/remove entry, set
visibility, create/update/delete table) unless the resolved viewer matches the `:user_id` path
param, and viewer resolution only happens when a bearer token is present
(services/game-room-api/authz/middleware.go's `ResolveViewer`); omitting the token here always
resolved the caller as anonymous, so every write 403'd regardless of who was actually logged in.
Reads pass it too, even though most are public - it costs nothing and lets a future logged-in
"friends" visibility resolution identify the viewer once friendship exists.
"""

import requests


class ShelfClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    @staticmethod
    def _headers(access_token: str | None) -> dict:
        return {"Authorization": f"Bearer {access_token}"} if access_token else {}

    def _get(self, path: str, access_token: str | None = None, **kwargs):
        resp = requests.get(
            f"{self.base_url}{path}", timeout=5, headers=self._headers(access_token), **kwargs
        )
        resp.raise_for_status()
        return resp.json()

    def _request(self, method: str, path: str, access_token: str | None = None, **kwargs):
        resp = requests.request(
            method, f"{self.base_url}{path}", timeout=5, headers=self._headers(access_token), **kwargs
        )
        resp.raise_for_status()
        if resp.content:
            return resp.json()
        return None

    # -- library --

    def get_library(self, user_id: str, access_token: str | None = None):
        return self._get(f"/users/{user_id}/library", access_token=access_token)

    def add_library_entry(self, user_id: str, volume_id: str, access_token: str | None = None):
        return self._request(
            "POST", f"/users/{user_id}/library/entries", access_token=access_token, json={"volume_id": volume_id}
        )

    def remove_library_entry(self, user_id: str, volume_id: str, access_token: str | None = None):
        return self._request(
            "DELETE", f"/users/{user_id}/library/entries/{volume_id}", access_token=access_token
        )

    def preview_library_default_visibility(self, user_id: str, visibility: str, access_token: str | None = None):
        return self._request(
            "POST",
            f"/users/{user_id}/library/default-visibility/preview",
            access_token=access_token,
            json={"visibility": visibility},
        )

    def set_library_default_visibility(
        self, user_id: str, visibility: str, overrides: dict | None = None, access_token: str | None = None
    ):
        payload = {"visibility": visibility}
        if overrides:
            payload["overrides"] = overrides
        return self._request(
            "PUT", f"/users/{user_id}/library/default-visibility", access_token=access_token, json=payload
        )

    def set_library_entry_visibility(
        self, user_id: str, volume_id: str, visibility: str | None, access_token: str | None = None
    ):
        return self._request(
            "PUT",
            f"/users/{user_id}/library/entries/{volume_id}/visibility",
            access_token=access_token,
            json={"visibility": visibility},
        )

    # -- wishlist --

    def get_wishlist(self, user_id: str, access_token: str | None = None):
        return self._get(f"/users/{user_id}/wishlist", access_token=access_token)

    def add_wishlist_entry(self, user_id: str, volume_id: str, access_token: str | None = None):
        return self._request(
            "POST", f"/users/{user_id}/wishlist/entries", access_token=access_token, json={"volume_id": volume_id}
        )

    def remove_wishlist_entry(self, user_id: str, volume_id: str, access_token: str | None = None):
        return self._request(
            "DELETE", f"/users/{user_id}/wishlist/entries/{volume_id}", access_token=access_token
        )

    def set_wishlist_visibility(self, user_id: str, visibility: str, access_token: str | None = None):
        return self._request(
            "PUT", f"/users/{user_id}/wishlist/visibility", access_token=access_token, json={"visibility": visibility}
        )

    # -- tables --

    def list_tables(self, user_id: str, access_token: str | None = None):
        return self._get(f"/users/{user_id}/tables", access_token=access_token)

    def get_table(self, user_id: str, table_id: str, access_token: str | None = None):
        return self._get(f"/users/{user_id}/tables/{table_id}", access_token=access_token)

    def create_table(self, user_id: str, name: str, visibility: str = "private", access_token: str | None = None):
        return self._request(
            "POST", f"/users/{user_id}/tables", access_token=access_token, json={"name": name, "visibility": visibility}
        )

    def update_table(self, user_id: str, table_id: str, name: str, visibility: str, access_token: str | None = None):
        return self._request(
            "PUT",
            f"/users/{user_id}/tables/{table_id}",
            access_token=access_token,
            json={"name": name, "visibility": visibility},
        )

    def delete_table(self, user_id: str, table_id: str, access_token: str | None = None):
        return self._request("DELETE", f"/users/{user_id}/tables/{table_id}", access_token=access_token)

    def add_table_volume(self, user_id: str, table_id: str, volume_id: str, access_token: str | None = None):
        return self._request(
            "POST",
            f"/users/{user_id}/tables/{table_id}/volumes",
            access_token=access_token,
            json={"volume_id": volume_id},
        )

    def remove_table_volume(
        self, user_id: str, table_id: str, volume_id: str, access_token: str | None = None
    ):
        return self._request(
            "DELETE", f"/users/{user_id}/tables/{table_id}/volumes/{volume_id}", access_token=access_token
        )
