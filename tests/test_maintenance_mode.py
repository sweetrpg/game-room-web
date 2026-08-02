# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""test_maintenance_mode.py

Covers the maintenance-mode before_request hook added to the main "web"
blueprint: it should short-circuit with a maintenance page when admin-api
reports an active maintenance-mode record for this app's scopes, stay
completely out of the way otherwise (including when admin-api is
unreachable, per the admin-api-client's fail-open contract), and never gate
the health-check routes so orchestration keeps seeing the pod as healthy.
"""

import pytest
from flask import Flask

from sweetrpg_shelf_web.application import constants
from sweetrpg_shelf_web.application.blueprints import blueprint as main_blueprint
from sweetrpg_web_core.blueprints.health import blueprint as health_blueprint


class FakeMaintenanceMode:
    """Stand-in for sweetrpg_admin_api_client.MaintenanceMode."""

    def __init__(
        self,
        label="Scheduled maintenance",
        description="We will be back shortly.",
        starts_at="2026-08-01T00:00:00Z",
        ends_at="2026-08-01T02:00:00Z",
    ):
        self.label = label
        self.description = description
        self.starts_at = starts_at
        self.ends_at = ends_at


class FakeAdminClient:
    """Stand-in for sweetrpg_admin_api_client.AdminClient.

    The real client never raises and returns [] on any failure (disabled
    client, timeout, network error, bad response) - that contract is
    exercised here by configuring the fake with no modes, rather than by
    hitting a real unreachable socket in a unit test.
    """

    def __init__(self, modes=None):
        self._modes = modes if modes is not None else []
        self.calls = []

    def fetch_maintenance_modes(self, scopes):
        self.calls.append(list(scopes))
        return self._modes


_health_registered = False


def _build_app(admin_client=None):
    global _health_registered
    if not _health_registered:
        # Mirrors create_app()'s one-time registration of the health
        # blueprint under the main blueprint.
        main_blueprint.register_blueprint(health_blueprint)
        _health_registered = True

    app = Flask("test_shelf_web")
    app.config["TESTING"] = True
    app.secret_key = "test-secret"
    if admin_client is not None:
        app.config[constants.ADMIN_API_CLIENT_KEY] = admin_client
    app.register_blueprint(main_blueprint)
    return app


@pytest.fixture
def app_factory():
    return _build_app


def test_maintenance_page_renders_when_active(app_factory):
    mode = FakeMaintenanceMode(label="Down for upgrades", description="Back soon.")
    admin_client = FakeAdminClient(modes=[mode])
    client = app_factory(admin_client).test_client()

    response = client.get("/")

    assert response.status_code == 503
    body = response.get_data(as_text=True)
    assert "Down for upgrades" in body
    assert "Back soon." in body
    assert admin_client.calls == [["platform", "service:shelf"]]


def test_normal_request_passes_through_when_no_active_maintenance(app_factory):
    admin_client = FakeAdminClient(modes=[])
    client = app_factory(admin_client).test_client()

    response = client.get("/")

    # This repo ships no templates dir, so "/" falls through to the
    # blueprint's generic error handler (500) - the behavior under test is
    # that the request was NOT short-circuited by the maintenance check.
    assert response.status_code != 503
    assert admin_client.calls == [["platform", "service:shelf"]]


def test_unreachable_admin_api_fails_open(app_factory):
    admin_client = FakeAdminClient(modes=[])
    client = app_factory(admin_client).test_client()

    response = client.get("/")

    assert response.status_code != 503


def test_missing_admin_client_does_not_block_requests(app_factory):
    client = app_factory(admin_client=None).test_client()

    response = client.get("/")

    assert response.status_code != 503


def test_health_check_stays_reachable_during_maintenance(app_factory):
    admin_client = FakeAdminClient(modes=[FakeMaintenanceMode()])
    client = app_factory(admin_client).test_client()

    response = client.get("/health/ping")

    assert response.status_code == 200
    assert response.data == b"pong"
    # The maintenance check must not even call admin-api for health routes.
    assert admin_client.calls == []
