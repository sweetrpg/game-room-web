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
    api_client = current_app.config[constants.API_CLIENT_KEY]
    volumes = api_client.query() # TODO
    context = get_context().update({'volumes': volumes})
    return render_template("volumes/index.html", **context)

@blueprint.route("/<id>", methods=["GET"])
def get_volume(id:str):
    api_client = current_app.config[constants.API_CLIENT_KEY]
    volume = api_client.get(id)
    if not volume:
        raise ObjectNotFound(id)
    context = get_context().update({'volume': volume})
    return render_template("volumes/single.html", **context)
