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


# -- wishlist --


def test_set_wishlist_visibility_calls_client(owner_client, client_mock):
    resp = owner_client.post("/wishlist/visibility", data={"visibility": "private"})
    assert resp.status_code == 302
    client_mock.set_wishlist_visibility.assert_called_once_with("user-1", "private")


def test_remove_wishlist_entry_calls_client(owner_client, client_mock):
    resp = owner_client.post("/wishlist/entries/vol-1", data={"_method": "DELETE"})
    assert resp.status_code == 302
    client_mock.remove_wishlist_entry.assert_called_once_with("user-1", "vol-1")


def test_get_wishlist_page_anonymous_shows_login_prompt(app):
    client = app.test_client()
    resp = client.get("/wishlist/")
    assert resp.status_code == 200


def test_get_user_wishlist_page_renders(owner_client, client_mock):
    client_mock.get_wishlist.return_value = {"user_id": "user-1", "entries": []}
    resp = owner_client.get("/wishlist/users/user-1")
    assert resp.status_code == 200


def test_get_wishlist_handles_client_error(owner_client, client_mock):
    client_mock.get_wishlist.side_effect = Exception("boom")
    resp = owner_client.get("/wishlist/")
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
