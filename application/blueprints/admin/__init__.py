__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
admin.py
- Administrative endpoints.
"""


from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException
from application.blueprints import requires_auth, render_page, error_page


blueprint = Blueprint("admin", __name__)


@blueprint.errorhandler(Exception)
def handle_error(ex):
    code = (ex.code if isinstance(ex, HTTPException) else 500)
    return error_page(str(ex), code)


@blueprint.route('/')
@requires_auth
def main_page():
    return render_page('admin/main.html')


@blueprint.route('/users')
@requires_auth
def settings():
    return render_page('admin/users.html')
