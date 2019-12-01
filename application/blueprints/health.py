__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
auth.py
- Authentication and authorization endpoints.
"""


from flask import Blueprint, current_app
import json
import os


blueprint = Blueprint("health", __name__)


@blueprint.route('/')
def health_check():
    with open(f'/{current_app.static_folder}/build-info.json', 'r') as bi:
        build_info = json.load(bi)
        return build_info


@blueprint.route('/ping')
def ping():
    return "pong"
