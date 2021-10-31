# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Volume routes.
"""

import functools
from flask import Blueprint, current_app, render_template, request, g
from sweetrpg_library_web.application import constants
from sweetrpg_web_core.helpers.context import get_context
from sweetrpg_client.types import VOLUME
from sweetrpg_client.exceptions import ObjectNotFound

blueprint = Blueprint("volumes", __name__, url_prefix="/volumes")


@blueprint.route("/", methods=["GET"])
def get_volumes():
    api_client = current_app.config[constants.LIBRARY_API_CLIENT_KEY]
    volumes = api_client.query(VOLUME) # TODO
    context = get_context().update({'volumes': volumes})
    return render_template("volumes/index.html", **context)


@blueprint.route("/<id>", methods=["GET"])
def get_volume(id:str):
    api_client = current_app.config[constants.LIBRARY_API_CLIENT_KEY]
    volume = api_client.get(VOLUME, id)
    if not volume:
        raise ObjectNotFound(id)
    context = get_context().update({'volume': volume})
    return render_template("volumes/single.html", **context)
