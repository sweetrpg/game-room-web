__author__ = "Paul Schifferer <dm@sweetrpg.com>"
__version__ = "1.0"
"""
"""

import sentry_sdk
import os
from application import constants
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration


sentry_sdk.init(dsn=os.environ[constants.SENTRY_DSN],
                integrations=[
                    FlaskIntegration(), SqlalchemyIntegration(), RedisIntegration()
                    ])
