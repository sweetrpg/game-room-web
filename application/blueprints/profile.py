__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
profile.py
- User profile endpoints.
"""


from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException
from . import render_page, requires_auth


blueprint = Blueprint("profile", __name__)


# @blueprint.errorhandler(Exception)
# def handle_auth_error(ex):
#     response = jsonify(message=str(ex))
#     response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
#     return response


@blueprint.route('/')
@requires_auth
def main_page():
    return render_page('profile/main.html')


@blueprint.route('/settings')
@requires_auth
def home_page():
    return render_page('profile/settings.html')
