__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
auth.py
- Authentication and authorization endpoints.
"""


from flask import Blueprint, current_app, jsonify
from werkzeug.exceptions import HTTPException
import json


blueprint = Blueprint("health", __name__)


# @blueprint.errorhandler(Exception)
# def handle_auth_error(ex):
#     response = jsonify(message=str(ex))
#     response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
#     return response


@blueprint.route('/')
def health_check():
    with open(f'/{current_app.static_folder}/build-info.json', 'r') as bi:
        build_info = json.load(bi)
        return build_info


@blueprint.route('/ping')
def ping():
    return "pong"
