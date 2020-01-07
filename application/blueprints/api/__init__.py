__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
- API
"""


from functools import wraps
from flask import Blueprint, request, render_template, session, jsonify, current_app
from werkzeug.exceptions import HTTPException
import json
import os
from application import constants
from application.models import constants as model_constants
from .. import render_page, requires_auth
from application.models.user import User
from application.utils.user import has_role


blueprint = Blueprint("api", __name__)


class UserAuthorizationException(Exception):
    def __init__(self, reason:str):
        self.reason = reason


def _check_user(role_name: str):
    user_id = session.get(constants.CURRENT_USER_ID)
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        if user:
            if has_role(user, role_name):
                return user

            raise UserAuthorizationException('insufficient permissions')

        raise UserAuthorizationException('user not found')

    raise UserAuthorizationException('no user in session')


def admin_required(f):
    @wraps(f)
    def _get_user(*args, **kwargs):
        try:
            user = _check_user(model_constants.ROLE_ADMIN)
            return f(user, *args, **kwargs)
        except UserAuthorizationException as e:
            return jsonify({
                'error': "Unauthorized; " + e.reason
            }), 401

    return _get_user


def user_required(f):
    @wraps(f)
    def _get_user(*args, **kwargs):
        try:
            user = _check_user(model_constants.ROLE_USER)
            return f(user, *args, **kwargs)
        except UserAuthorizationException as e:
            return jsonify({
                'error': "Unauthorized; " + e.reason
            }), 401

    return _get_user


def user_optional(f):
    @wraps(f)
    def _get_user(*args, **kwargs):
        try:
            user = _check_user(model_constants.ROLE_USER)
            return f(user, *args, **kwargs)
        except UserAuthorizationException as e:
            return f(None, *args, **kwargs)

    return _get_user


@blueprint.errorhandler(Exception)
def error_handler(ex):
    current_app.logger.exception(f"Exception caught: {ex}")
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


from application.blueprints.api.common import game_systems, utils
from application.blueprints.api.initiative import encounters, groups
