__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

import os
from authlib.flask.client import OAuth
from application import constants
from flask import current_app


oauth = OAuth(current_app)

auth0 = oauth.register(
    'auth0',
    client_id=os.environ[constants.AUTH0_CLIENT_ID],
    client_secret=os.environ[constants.AUTH0_CLIENT_SECRET],
    api_base_url=os.environ[constants.AUTH0_DOMAIN],
    access_token_url=os.environ[constants.AUTH0_DOMAIN] + '/oauth/token',
    authorize_url=os.environ[constants.AUTH0_DOMAIN] + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)
