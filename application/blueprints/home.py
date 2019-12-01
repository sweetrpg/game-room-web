__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
auth.py
- Authentication and authorization endpoints.
"""


from flask import Blueprint, render_template
import json
import os


blueprint = Blueprint("home", __name__)


@blueprint.route('/')
def main_page():
    # with open(f'build-info.json', 'r') as bi:
    #     build_info = json.load(bi)
    #     return build_info
    return render_template('index.html')


@blueprint.route('/home')
def home_page():
    return render_template('home.html')
