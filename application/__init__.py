__author__ = "Paul Schifferer <dm@sweetrpg.com>"
__version__ = "1.0"

import sentry_sdk
import os
import application.constants


sentry_sdk.init(os.environ[constants.SENTRY_DSN])
