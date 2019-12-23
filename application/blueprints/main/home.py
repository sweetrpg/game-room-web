__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
auth.py
- Authentication and authorization endpoints.
"""


from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException
from application.blueprints import requires_auth, render_page, error_page
from application.cache import cache


blueprint = Blueprint("home", __name__)


@blueprint.errorhandler(Exception)
def handle_error(ex):
    code = (ex.code if isinstance(ex, HTTPException) else 500)
    return error_page(str(ex), code)


@blueprint.route('/')
# @cache.cached(timeout=50)
def main_page():
    """
    Main application page, with generic non-user stuff.
    """
    return render_page('index.html')


@blueprint.route('/home')
@requires_auth
# @cache.cached(timeout=50)
def home_page():
    """
    Personal page for the user, with application usage info, etc.
    """
    return render_page('home.html')
