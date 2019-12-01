__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
auth.py
- Authentication and authorization endpoints.
"""


from flask import Blueprint, render_template, session
import json
import os
from application import constants
from . import requires_auth, render_page


blueprint = Blueprint("home", __name__)


@blueprint.route('/')
def main_page():
    """
    Main application page, with generic non-user stuff.
    """
    return render_page('index.html')


@blueprint.route('/home')
@requires_auth
def home_page():
    """
    Personal page for the user, with application usage info, etc.
    """
    return render_page('home.html')
