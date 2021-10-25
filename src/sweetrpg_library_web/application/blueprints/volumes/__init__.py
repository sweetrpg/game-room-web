# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Volume routes.
"""

import functools
from flask import Blueprint, current_app, render_template, request, g
from sweetrpg_library_web.application import constants
from sweetrpg_web_core.helpers.context import get_context


blueprint = Blueprint("volumes", __name__, url_prefix="/volumes")


@blueprint.route("/", methods=["GET"])
def get_volumes():
    api_client = g[constants.API_CLIENT_KEY]
    context = get_context().update({'volumes':[]})
    return render_template("volumes/index.html", **context)

@blueprint.route("/<id>", methods=["GET"])
def get_volume(id:str):
    api_client = g[constants.API_CLIENT_KEY]
    context = {}
    return render_template("volumes/single.html", **context)
