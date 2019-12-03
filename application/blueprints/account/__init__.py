__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
account.py
- User account endpoints.
"""


from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException
from application.blueprints import requires_auth, render_page


blueprint = Blueprint("account", __name__)


# @blueprint.errorhandler(Exception)
# def handle_auth_error(ex):
#     response = jsonify(message=str(ex))
#     response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
#     return response


@blueprint.route('/')
@requires_auth
def main_page():
    return render_page('account/main.html')


@blueprint.route('/settings')
@requires_auth
def settings():
    return render_page('account/settings.html')


@blueprint.route('/email')
@requires_auth
def change_email_request():
    return render_page('account/email.html')
