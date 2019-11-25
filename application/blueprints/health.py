__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
auth.py
- Authentication and authorization endpoints.
"""


from flask import Blueprint
import json


blueprint = Blueprint("health", __name__)



@blueprint.route('/')
def health_check():
    with open('/static/build-info.json', 'r') as bi:
        build_info = json.load(bi)
        return build_info


@blueprint.route('/ping')
def ping():
    return "pong"
