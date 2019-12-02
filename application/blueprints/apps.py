__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
apps.py
- Applications.
"""


from flask import Blueprint, render_template, session, jsonify
from werkzeug.exceptions import HTTPException
import json
import os
from application import constants
from . import render_page, requires_auth


blueprint = Blueprint("apps", __name__)


# @blueprint.errorhandler(Exception)
# def handle_auth_error(ex):
#     response = jsonify(message=str(ex))
#     response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
#     return response


@blueprint.route('/initiative')
@requires_auth
def initiative_app():
    return render_page('apps/initiative/main.html')
