__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
- API
"""


from flask import Blueprint, render_template, session, jsonify
from werkzeug.exceptions import HTTPException
import json
import os
from application import constants
from .. import render_page, requires_auth


blueprint = Blueprint("api", __name__)

@blueprint.errorhandler(Exception)
def error_handler(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


from .initiative import encounters
