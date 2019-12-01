__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
apps.py
- Applications.
"""


from flask import Blueprint, render_template, session
import json
import os
from application import constants
from . import render_page, requires_auth


blueprint = Blueprint("apps", __name__)


@blueprint.route('/initiative')
@requires_auth
def initiative_app():
    return render_page('apps/initiative.html')
