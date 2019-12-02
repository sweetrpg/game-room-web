__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
auth.py
- Authentication and authorization endpoints.
"""


from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException
from . import requires_auth, render_page


blueprint = Blueprint("home", __name__)


@blueprint.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


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
