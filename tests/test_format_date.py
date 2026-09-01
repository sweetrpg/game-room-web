# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Tests for blueprints._format_date."""

import pytest

from sweetrpg_game_room_web.application.blueprints import _format_date


@pytest.mark.parametrize("value", [None, "", "not-a-date"])
def test_missing_or_unparseable_returns_none(value):
    assert _format_date(value) is None


@pytest.mark.parametrize(
    "value",
    [
        "0001-01-01T00:00:00Z",       # Go zero time
        "0001-01-01T00:00:00+00:00",
        "1970-01-01T00:00:00+00:00",  # Unix epoch
    ],
)
def test_zero_value_sentinels_return_none(value):
    assert _format_date(value) is None


def test_real_date_is_formatted():
    assert _format_date("2026-08-28T12:00:00+00:00") == "Aug 28, 2026"
