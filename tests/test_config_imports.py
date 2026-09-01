# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Guard: config.BaseConfig class body must evaluate without error.

Every attribute is resolved at class-definition time, so a dangling
`constants.X` reference is an import-time AttributeError that crashes uWSGI
before any request (regression: `constants.SEGMENT_WRITE_KEY` removed while
`config.py` still referenced it).
"""


def test_base_config_evaluates():
    from sweetrpg_game_room_web.application.config import BaseConfig

    assert hasattr(BaseConfig, "SEGMENT_WRITE_KEY")
    assert hasattr(BaseConfig, "USERS_API_URL")
