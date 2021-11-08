# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Volume routes.
"""

import functools
from flask import Blueprint, current_app, render_template, request, g, flash
from sweetrpg_library_web.application import constants
from sweetrpg_web_core.helpers.context import get_context
from sweetrpg_client.types import VOLUME
from sweetrpg_client.exceptions import NotFound
from jsonapi_client import Session
import os


blueprint = Blueprint("volumes", __name__, url_prefix="/volumes")


@blueprint.route("/", methods=["GET"])
def get_volumes():
    context = get_context()
    current_app.logger.debug("context: %s", context)
    # api_client = current_app.config[constants.SWEETRPG_API_CLIENT_KEY]
    # volumes = api_client.query(VOLUME) # TODO
    try:
        with Session(f"{os.environ[constants.LIBRARY_API_BASE_URL]}") as s:
            volumes = s.get("volumes")
            current_app.logger.debug("volumes: %s", volumes)
            context.update({'volumes': volumes})
    except:
        current_app.logger.exception("Unable to fetch volumes!")
        flash('Unable to fetch volumes!')

    return render_template("volumes/index.html", **context)


@blueprint.route("/<id>", methods=["GET"])
def get_volume(id:str):
    api_client = current_app.config[constants.SWEETRPG_API_CLIENT_KEY]
    volume = api_client.get(VOLUME, id)
    if not volume:
        raise NotFound(id)
    context = get_context().update({'volume': volume})
    return render_template("volumes/single.html", **context)
