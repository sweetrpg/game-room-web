__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
- API
"""


from functools import wraps
from flask import Blueprint, request, render_template, session, jsonify
from werkzeug.exceptions import HTTPException
import json
import os
from application import constants
from .. import render_page, requires_auth
from application.models.user import User


blueprint = Blueprint("api", __name__)


def user_required(f):
    @wraps(f)
    def _get_user(*args, **kwargs):
        user_id = session.get(constants.CURRENT_USER_ID)
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if user:
                return f(user, *args, **kwargs)

        return jsonify({
            'error': "Invalid session, no user found"
        }), 401

    return _get_user


@blueprint.errorhandler(Exception)
def error_handler(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


from .common import game_systems, utils
from .initiative import encounters
