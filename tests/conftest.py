# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""conftest.py

Sets required environment variables before any `sweetrpg_game_room_web` module is
imported. `sweetrpg_game_room_web.application` initializes Sentry at import time
and reads `SENTRY_DSN` unconditionally, so it must be present (even if empty)
for any test that imports the application package - this has nothing to do
with the behavior under test.
"""

import os

os.environ.setdefault("SENTRY_DSN", "")
os.environ.setdefault("SENTRY_ENV", "test")
os.environ.setdefault("REDIS_HOST", "localhost")
os.environ.setdefault("GAME_ROOM_API_BASE_URL", "http://localhost:9999")
