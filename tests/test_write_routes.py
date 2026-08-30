# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Tests for the library/wishlist/tables POST (write) routes.

These use main_blueprint ("web") nesting - unlike test_viewer_routes.py's direct
sub-blueprint registration - because every redirect target here is
`url_for("web.<blueprint>.<endpoint>")`, which only resolves under that nesting.
That nesting also pulls in the "web" blueprint's `_populate` before_request hook,
which derives identity from `shared_session.current_user()` (the suite-wide login
session), overwriting the Flask session on every request - so the owner fixture
patches that lookup rather than seeding the session directly.
"""

import os
from unittest.mock import MagicMock, patch

import pytest
from flask import Flask

from sweetrpg_game_room_web.application import constants
from sweetrpg_game_room_web.application.blueprints import blueprint as main_blueprint
from sweetrpg_game_room_web.application.blueprints.library import blueprint as library_blueprint
from sweetrpg_game_room_web.application.blueprints.wishlist import blueprint as wishlist_blueprint
from sweetrpg_game_room_web.application.blueprints.tables import blueprint as tables_blueprint

TEMPLATE_DIR = os.path.join(
    os.path.dirname(__file__), "..", "src", "sweetrpg_game_room_web", "application", "templates"
)

# main_blueprint is a module-level singleton; register its sub-blueprints once at
# import time rather than per-test, or Flask raises on the second attempt ("blueprint
# has already been registered - the setup method 'register_blueprint' can no longer
# be called").
main_blueprint.register_blueprint(library_blueprint)
main_blueprint.register_blueprint(wishlist_blueprint)
main_blueprint.register_blueprint(tables_blueprint)


class _OwnerClient:
    """Wraps a Flask test client, faking a valid shared-session user for every request."""

    def __init__(self, client, user_id):
        self._client = client
        self._user_id = user_id

    def get(self, *args, **kwargs):
        return self._request("get", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._request("post", *args, **kwargs)

    def _request(self, method, *args, **kwargs):
        with patch(
            "sweetrpg_game_room_web.application.blueprints.shared_session.current_user",
            return_value={"sub": self._user_id, "email": f"{self._user_id}@example.com"},
        ):
            return getattr(self._client, method)(*args, **kwargs)


@pytest.fixture
def client_mock():
    return MagicMock()


@pytest.fixture
def app(client_mock):
    app = Flask(__name__, template_folder=TEMPLATE_DIR)
    app.config["SECRET_KEY"] = "test"
    app.register_blueprint(main_blueprint)

    app.config[constants.GAME_ROOM_CLIENT_KEY] = client_mock
    app.config[constants.CATALOG_CLIENT_KEY] = client_mock
    with patch("sweetrpg_game_room_web.application.blueprints.analytics.identify"), patch(
        "sweetrpg_game_room_web.application.blueprints.analytics.track"
    ):
        yield app


@pytest.fixture
def owner_client(app):
    return _OwnerClient(app.test_client(), "user-1")


# -- tracking --


def test_track_skips_analytics_when_write_key_unset(owner_client):
    with patch("sweetrpg_game_room_web.application.blueprints.analytics.write_key", None), patch(
        "sweetrpg_game_room_web.application.blueprints.analytics.identify"
    ) as identify:
        owner_client.get("/library/")
        identify.assert_not_called()


def test_track_calls_analytics_when_write_key_set(owner_client):
    with patch("sweetrpg_game_room_web.application.blueprints.analytics.write_key", "test-key"), patch(
        "sweetrpg_game_room_web.application.blueprints.analytics.identify"
    ) as identify:
        owner_client.get("/library/")
        identify.assert_called_once()


# -- library --


def test_set_default_visibility_calls_client_and_redirects(owner_client, client_mock):
    resp = owner_client.post("/library/default-visibility", data={"visibility": "public"})
    assert resp.status_code == 302
    assert resp.location.endswith("/library/")
    client_mock.set_library_default_visibility.assert_called_once_with("user-1", "public", None)


def test_set_default_visibility_handles_client_error(owner_client, client_mock):
    client_mock.set_library_default_visibility.side_effect = Exception("boom")
    resp = owner_client.post("/library/default-visibility", data={"visibility": "public"})
    assert resp.status_code == 302


def test_set_entry_visibility_calls_client(owner_client, client_mock):
    resp = owner_client.post("/library/entries/vol-1/visibility", data={"visibility": "friends"})
    assert resp.status_code == 302
    client_mock.set_library_entry_visibility.assert_called_once_with("user-1", "vol-1", "friends")


def test_remove_library_entry_requires_delete_method_override(owner_client, client_mock):
    resp = owner_client.post("/library/entries/vol-1", data={"_method": "DELETE"})
    assert resp.status_code == 302
    client_mock.remove_library_entry.assert_called_once_with("user-1", "vol-1")


def test_remove_library_entry_ignored_without_delete_override(owner_client, client_mock):
    resp = owner_client.post("/library/entries/vol-1", data={})
    assert resp.status_code == 302
    client_mock.remove_library_entry.assert_not_called()


def test_search_volumes_returns_empty_list_for_blank_query(owner_client, client_mock):
    resp = owner_client.get("/library/volume-search?q=")
    assert resp.status_code == 200
    assert resp.get_json() == []
    client_mock.search_volumes.assert_not_called()


def test_search_volumes_calls_catalog_client(owner_client, client_mock):
    client_mock.search_volumes.return_value = [{"id": "vol-1", "title": "Curse of Strahd"}]
    resp = owner_client.get("/library/volume-search?q=Curse")
    assert resp.status_code == 200
    assert resp.get_json() == [{"id": "vol-1", "title": "Curse of Strahd"}]
    client_mock.search_volumes.assert_called_once_with("Curse")


def test_search_volumes_handles_client_error(owner_client, client_mock):
    client_mock.search_volumes.side_effect = Exception("boom")
    resp = owner_client.get("/library/volume-search?q=Curse")
    assert resp.status_code == 502
    assert resp.get_json() == []


def test_add_entry_requires_volume_id(owner_client, client_mock):
    resp = owner_client.post("/library/entries", json={"volume_id": ""})
    assert resp.status_code == 400
    client_mock.add_library_entry.assert_not_called()


def test_add_entry_returns_updated_count_and_recent(owner_client, client_mock):
    client_mock.get_library.return_value = {
        "entries": [{"volume_id": "vol-1", "added_at": "2026-08-28T12:00:00+00:00"}]
    }
    resp = owner_client.post("/library/entries", json={"volume_id": "vol-1"})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["count"] == 1
    assert body["recent"][0]["volume_id"] == "vol-1"
    client_mock.add_library_entry.assert_called_once_with("user-1", "vol-1")


def test_add_entry_handles_client_error(owner_client, client_mock):
    client_mock.add_library_entry.side_effect = Exception("boom")
    resp = owner_client.post("/library/entries", json={"volume_id": "vol-1"})
    assert resp.status_code == 502
    assert "error" in resp.get_json()


# -- wishlist --


def test_create_wishlist_requires_name(owner_client, client_mock):
    resp = owner_client.post("/wishlist/", data={"name": ""})
    assert resp.status_code == 302
    assert resp.location.endswith("/wishlist/new")
    client_mock.create_wishlist.assert_not_called()


def test_create_wishlist_success_redirects_to_detail(owner_client, client_mock):
    client_mock.create_wishlist.return_value = {"id": "wl-1"}
    resp = owner_client.post("/wishlist/", data={"name": "Holiday", "visibility": "private"})
    assert resp.status_code == 302
    assert resp.location.endswith("/wishlist/wl-1")
    client_mock.create_wishlist.assert_called_once_with("user-1", "Holiday", "private")


def test_create_wishlist_redirect_carries_base_path_prefix(owner_client, client_mock):
    """Regression test: wishlist in-app redirects must carry APPLICATION_BASE_PATH
    (see local_redirect in blueprints/__init__.py)."""
    client_mock.create_wishlist.return_value = {"id": "wl-1"}
    with patch.dict(os.environ, {"APPLICATION_BASE_PATH": "/game-room"}):
        resp = owner_client.post("/wishlist/", data={"name": "Holiday", "visibility": "private"})
    assert resp.location == "/game-room/wishlist/wl-1"


def test_create_wishlist_handles_client_error(owner_client, client_mock):
    client_mock.create_wishlist.side_effect = Exception("boom")
    resp = owner_client.post("/wishlist/", data={"name": "Holiday"})
    assert resp.status_code == 302
    assert resp.location.endswith("/wishlist/new")


def test_update_wishlist_deletes_when_method_override_set(owner_client, client_mock):
    resp = owner_client.post("/wishlist/wl-1", data={"_method": "DELETE"})
    assert resp.status_code == 302
    assert resp.location.endswith("/wishlist/")
    client_mock.delete_wishlist.assert_called_once_with("user-1", "wl-1")


def test_update_wishlist_sets_visibility(owner_client, client_mock):
    resp = owner_client.post("/wishlist/wl-1", data={"visibility": "public"})
    assert resp.status_code == 302
    assert resp.location.endswith("/wishlist/wl-1")
    client_mock.set_wishlist_visibility.assert_called_once_with("user-1", "wl-1", "public")


def test_update_wishlist_handles_client_error(owner_client, client_mock):
    client_mock.set_wishlist_visibility.side_effect = Exception("boom")
    resp = owner_client.post("/wishlist/wl-1", data={"visibility": "public"})
    assert resp.status_code == 302
    assert resp.location.endswith("/wishlist/wl-1")


def test_delete_wishlist_handles_client_error(owner_client, client_mock):
    client_mock.delete_wishlist.side_effect = Exception("boom")
    resp = owner_client.post("/wishlist/wl-1", data={"_method": "DELETE"})
    assert resp.status_code == 302
    assert resp.location.endswith("/wishlist/")


def test_add_wishlist_entry_form_calls_client_when_volume_id_present(owner_client, client_mock):
    resp = owner_client.post("/wishlist/wl-1/entries", data={"volume_id": "vol-1"})
    assert resp.status_code == 302
    client_mock.add_wishlist_entry.assert_called_once_with("user-1", "wl-1", "vol-1")


def test_add_wishlist_entry_form_skipped_without_volume_id(owner_client, client_mock):
    resp = owner_client.post("/wishlist/wl-1/entries", data={})
    assert resp.status_code == 302
    client_mock.add_wishlist_entry.assert_not_called()


def test_add_wishlist_entry_form_handles_client_error(owner_client, client_mock):
    client_mock.add_wishlist_entry.side_effect = Exception("boom")
    resp = owner_client.post("/wishlist/wl-1/entries", data={"volume_id": "vol-1"})
    assert resp.status_code == 302
    assert resp.location.endswith("/wishlist/wl-1")


def test_remove_wishlist_entry_required_delete_method_override(owner_client, client_mock):
    resp = owner_client.post("/wishlist/wl-1/entries/vol-1", data={"_method": "DELETE"})
    assert resp.status_code == 302
    client_mock.remove_wishlist_entry.assert_called_once_with("user-1", "wl-1", "vol-1")


def test_remove_wishlist_entry_ignored_without_delete_override(owner_client, client_mock):
    resp = owner_client.post("/wishlist/wl-1/entries/vol-1", data={})
    assert resp.status_code == 302
    client_mock.remove_wishlist_entry.assert_not_called()


def test_remove_wishlist_entry_handles_client_error(owner_client, client_mock):
    client_mock.remove_wishlist_entry.side_effect = Exception("boom")
    resp = owner_client.post("/wishlist/wl-1/entries/vol-1", data={"_method": "DELETE"})
    assert resp.status_code == 302
    assert resp.location.endswith("/wishlist/wl-1")


# -- wishlist pages --


def test_get_wishlist_page_anonymous_shows_login_prompt(app):
    client = app.test_client()
    resp = client.get("/wishlist/")
    assert resp.status_code == 200
    assert "Log in to see your wishlists." in resp.get_data(as_text=True)


def test_get_wishlists_page_lists_wishlists(owner_client, client_mock):
    client_mock.list_wishlists.return_value = [{"id": "wl-1", "name": "Holiday", "entries": []}]
    resp = owner_client.get("/wishlist/")
    assert resp.status_code == 200
    client_mock.list_wishlists.assert_called_once_with("user-1")


def test_get_wishlists_page_handles_client_error(owner_client, client_mock):
    client_mock.list_wishlists.side_effect = Exception("boom")
    resp = owner_client.get("/wishlist/")
    assert resp.status_code == 200


def test_get_user_wishlists_page_lists_wishlists(owner_client, client_mock):
    client_mock.list_wishlists.return_value = [{"id": "wl-1", "name": "Holiday", "entries": []}]
    resp = owner_client.get("/wishlist/users/user-1")
    assert resp.status_code == 200


def test_get_wishlist_page_renders_detail(owner_client, client_mock):
    client_mock.get_wishlist.return_value = {"user_id": "user-1", "visibility": "private", "entries": []}
    resp = owner_client.get("/wishlist/wl-1")
    assert resp.status_code == 200
    assert 'id="visibility-menu-trigger"' in resp.get_data(as_text=True)


def test_get_user_wishlist_page_renders_detail(owner_client, client_mock):
    client_mock.get_wishlist.return_value = {"user_id": "user-2", "visibility": "private", "entries": []}
    resp = owner_client.get("/wishlist/users/user-2/wl-1")
    assert resp.status_code == 200


def test_get_wishlist_page_handles_client_error(owner_client, client_mock):
    client_mock.get_wishlist.side_effect = Exception("boom")
    resp = owner_client.get("/wishlist/wl-1")
    assert resp.status_code == 200


def test_new_wishlist_page_renders(owner_client):
    resp = owner_client.get("/wishlist/new")
    assert resp.status_code == 200


# -- tables --


def test_new_table_page_renders(owner_client):
    resp = owner_client.get("/tables/new")
    assert resp.status_code == 200


def test_create_table_requires_name(owner_client, client_mock):
    resp = owner_client.post("/tables/", data={"name": ""})
    assert resp.status_code == 302
    assert resp.location.endswith("/tables/new")
    client_mock.create_table.assert_not_called()


def test_create_table_success_redirects_to_detail(owner_client, client_mock):
    client_mock.create_table.return_value = {"id": "table-1"}
    resp = owner_client.post("/tables/", data={"name": "Campaign Night", "visibility": "private"})
    assert resp.status_code == 302
    assert resp.location.endswith("/tables/table-1")
    client_mock.create_table.assert_called_once_with("user-1", "Campaign Night", "private")


def test_create_table_redirect_carries_base_path_prefix(owner_client, client_mock):
    """Regression test: redirect(url_for(...)) alone produces an unprefixed Location -
    Traefik strips APPLICATION_BASE_PATH before the request reaches this app (see
    docs/deployment-conventions.md), so the app's internal route table is unprefixed, but a
    redirect's Location header is resolved by the browser against the external, prefixed URL.
    """
    client_mock.create_table.return_value = {"id": "table-1"}
    with patch.dict(os.environ, {"APPLICATION_BASE_PATH": "/game-room"}):
        resp = owner_client.post("/tables/", data={"name": "Campaign Night", "visibility": "private"})
    assert resp.location == "/game-room/tables/table-1"


def test_create_table_handles_client_error(owner_client, client_mock):
    client_mock.create_table.side_effect = Exception("boom")
    resp = owner_client.post("/tables/", data={"name": "Campaign Night"})
    assert resp.status_code == 302
    assert resp.location.endswith("/tables/new")


def test_get_table_page_renders(owner_client, client_mock):
    client_mock.get_table.return_value = {"id": "table-1", "name": "Campaign Night", "volumes": []}
    resp = owner_client.get("/tables/table-1")
    assert resp.status_code == 200


def test_get_user_table_page_renders(owner_client, client_mock):
    client_mock.get_table.return_value = {"id": "table-1", "name": "Campaign Night", "volumes": []}
    resp = owner_client.get("/tables/users/user-2/table-1")
    assert resp.status_code == 200


def test_update_table_deletes_when_method_override_set(owner_client, client_mock):
    resp = owner_client.post("/tables/table-1", data={"_method": "DELETE"})
    assert resp.status_code == 302
    assert resp.location.endswith("/tables/")
    client_mock.delete_table.assert_called_once_with("user-1", "table-1")


def test_update_table_updates_name_and_visibility(owner_client, client_mock):
    resp = owner_client.post("/tables/table-1", data={"name": "New Name", "visibility": "public"})
    assert resp.status_code == 302
    assert resp.location.endswith("/tables/table-1")
    client_mock.update_table.assert_called_once_with("user-1", "table-1", "New Name", "public")


def test_add_volume_calls_client_when_volume_id_present(owner_client, client_mock):
    resp = owner_client.post("/tables/table-1/volumes", data={"volume_id": "vol-1"})
    assert resp.status_code == 302
    client_mock.add_table_volume.assert_called_once_with("user-1", "table-1", "vol-1")


def test_add_volume_skipped_without_volume_id(owner_client, client_mock):
    resp = owner_client.post("/tables/table-1/volumes", data={})
    assert resp.status_code == 302
    client_mock.add_table_volume.assert_not_called()


def test_remove_volume_calls_client(owner_client, client_mock):
    resp = owner_client.post("/tables/table-1/volumes/vol-1", data={"_method": "DELETE"})
    assert resp.status_code == 302
    client_mock.remove_table_volume.assert_called_once_with("user-1", "table-1", "vol-1")


def test_get_tables_page_lists_tables(owner_client, client_mock):
    client_mock.list_tables.return_value = [{"id": "table-1", "name": "Campaign Night"}]
    resp = owner_client.get("/tables/")
    assert resp.status_code == 200


def test_get_tables_page_handles_client_error(owner_client, client_mock):
    client_mock.list_tables.side_effect = Exception("boom")
    resp = owner_client.get("/tables/")
    assert resp.status_code == 200


# -- landing page --


def test_anonymous_visitor_sees_login_prompt_no_cards(app):
    with patch(
        "sweetrpg_game_room_web.application.blueprints.shared_session.current_user",
        return_value=None,
    ):
        resp = app.test_client().get("/")
    body = resp.get_data(as_text=True)
    assert "Log in to see your library" in body
    assert 'class="stat-card"' not in body


def test_logged_in_visitor_sees_library_wishlist_tables_cards(owner_client, client_mock):
    client_mock.get_library.return_value = {
        "entries": [
            {"volume_id": "vol-1", "added_at": "2026-08-28T12:00:00+00:00"},
            {"volume_id": "vol-2", "added_at": "2026-08-27T12:00:00+00:00"},
        ]
    }
    client_mock.list_wishlists.return_value = [
        {"id": "wl-1", "entries": [{"volume_id": "vol-3", "added_at": "2026-08-26T12:00:00+00:00"}]}
    ]
    client_mock.list_tables.return_value = [
        {"id": "table-1", "name": "Friday Night", "updated_at": "2026-08-25T12:00:00+00:00"}
    ]

    resp = owner_client.get("/")

    body = resp.get_data(as_text=True)
    assert 'class="stat-card"' in body
    assert "Log in to see your library" not in body
    assert "vol-1" in body
    assert "vol-3" in body
    assert "Friday Night" in body
    assert 'id="add-to-library-btn"' in body
    assert 'id="create-wishlist-btn"' in body
    assert 'id="create-table-btn"' in body
    client_mock.get_library.assert_called_once_with("user-1")
    client_mock.list_wishlists.assert_called_once_with("user-1")
    client_mock.list_tables.assert_called_once_with("user-1")


def test_logged_in_visitor_wishlist_count_aggregates_entries(owner_client, client_mock):
    client_mock.get_library.return_value = {"entries": []}
    client_mock.list_wishlists.return_value = [
        {"id": "wl-1", "entries": [{"volume_id": "vol-1", "added_at": "2026-08-26T12:00:00+00:00"}]},
        {
            "id": "wl-2",
            "entries": [
                {"volume_id": "vol-2", "added_at": "2026-08-25T12:00:00+00:00"},
                {"volume_id": "vol-3", "added_at": "2026-08-24T12:00:00+00:00"},
            ],
        },
    ]
    client_mock.list_tables.return_value = []

    resp = owner_client.get("/")

    body = resp.get_data(as_text=True)
    assert 'class="stat-card-count">3' in body


def test_anonymous_visitor_sees_no_card_action_buttons(app):
    with patch(
        "sweetrpg_game_room_web.application.blueprints.shared_session.current_user",
        return_value=None,
    ):
        resp = app.test_client().get("/")
    body = resp.get_data(as_text=True)
    assert 'id="add-to-library-btn"' not in body
    assert 'id="create-wishlist-btn"' not in body
    assert 'id="create-table-btn"' not in body


def test_logged_in_visitor_with_no_data_sees_empty_states(owner_client, client_mock):
    client_mock.get_library.return_value = {"entries": []}
    client_mock.list_wishlists.return_value = []
    client_mock.list_tables.return_value = []

    resp = owner_client.get("/")

    body = resp.get_data(as_text=True)
    assert "No volumes yet" in body
    assert "No entries yet" in body
    assert "No tables yet" in body


def test_logged_in_visitor_survives_client_errors(owner_client, client_mock):
    client_mock.get_library.side_effect = Exception("boom")
    client_mock.list_wishlists.side_effect = Exception("boom")
    client_mock.list_tables.side_effect = Exception("boom")

    resp = owner_client.get("/")

    assert resp.status_code == 200
    assert "No volumes yet" in resp.get_data(as_text=True)
