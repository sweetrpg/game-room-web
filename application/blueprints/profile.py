__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
profile.py
- User profile endpoints.
"""


from flask import Blueprint, render_template, session
import json
import os
from application import constants
from . import render_page


blueprint = Blueprint("profile", __name__)


@blueprint.route('/')
def main_page():
    return render_page('profile.html')


@blueprint.route('/settings')
def home_page():
    return render_page('settings.html')
