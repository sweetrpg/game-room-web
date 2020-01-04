__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
billing/__init__.py
- Payment and billing endpoints
"""


from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, current_app, redirect, session, url_for
from werkzeug.exceptions import HTTPException
from urllib.parse import urlencode
import jwt
from application.models.user import User
from application import constants
from application.utils.oauth import auth0
import os
from application.models.user import User
from application.db import db
from application.cache import cache


blueprint = Blueprint("billing", __name__)


from . import stripe
