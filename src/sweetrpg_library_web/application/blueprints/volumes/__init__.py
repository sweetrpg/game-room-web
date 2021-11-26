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
import os
from sweetrpg_library_web.application.blueprints import render_page


blueprint = Blueprint("volumes", __name__, url_prefix="/volumes")


@blueprint.route("/", methods=["GET"])
def get_volumes():
    """Get all volumes.

    """
    context = get_context()
    current_app.logger.debug("context: %s", context)
    api_client = current_app.config[constants.SWEETRPG_API_CLIENT_KEY]
    try:
        # url = os.environ[constants.LIBRARY_API_BASE_URL]
        # current_app.logger.debug("(LIBRARY_API_BASE_URL) url: %s", url)
        volumes = api_client.query(VOLUME)
        context.update({'volumes': volumes})
    except:
        current_app.logger.exception("Unable to fetch volumes!")
        flash('Unable to fetch volumes!')

    return render_page("apps/library/volumes/many.html", context=context)


@blueprint.route("/<id>", methods=["GET"])
def get_volume(id:str):
    """Get a specific volume.

    """
    context = get_context()
    current_app.logger.debug("context: %s", context)
    api_client = current_app.config[constants.SWEETRPG_API_CLIENT_KEY]
    try:
        volume = api_client.get(VOLUME, id)
        context.update({'volume': volume})
    except:
        current_app.logger.exception(f"Unable to fetch volume {id}!")
        flash(f'Unable to fetch volume {id}!')

    return render_page("apps/library/volumes/single.html", context=context)
