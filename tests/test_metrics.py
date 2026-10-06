# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Regression test for the /metrics endpoint: the PodMonitor
(kubernetes/overlays/dev/pod-monitor.yaml) scrapes it by default path, so a missing route here
means every scrape silently fails rather than erroring loudly.
"""

from flask import Flask

from sweetrpg_game_room_web.application.metrics import setup_metrics


def test_setup_metrics_registers_metrics_endpoint():
    app = Flask(__name__)
    setup_metrics(app)
    client = app.test_client()

    resp = client.get("/metrics")

    assert resp.status_code == 200
    assert b"python_gc_objects_collected_total" in resp.data
