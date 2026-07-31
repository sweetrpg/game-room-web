# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""License routes.
"""

import functools
from flask import Blueprint, current_app, render_template, request, g, flash
from sweetrpg_shelf_web.application import constants
from sweetrpg_web_core.helpers.context import get_context
from sweetrpg_client.types import LICENSE
from sweetrpg_client.exceptions import NotFound
import os
from sweetrpg_shelf_web.application.blueprints import render_page


blueprint = Blueprint("licenses", __name__, url_prefix="/licenses")


@blueprint.route("/", methods=["GET"])
def get_licenses_page():
    """Get all licenses page."""
    context = get_context()
    current_app.logger.debug("context: %s", context)
    # api_client = current_app.config[constants.SWEETRPG_API_CLIENT_KEY]
    # try:
    #     # url = os.environ[constants.SHELF_API_BASE_URL]
    #     # current_app.logger.debug("(SHELF_API_BASE_URL) url: %s", url)
    #     licenses = api_client.query(LICENSE)
    #     context.update({'licenses': licenses})
    # except:
    #     current_app.logger.exception("Unable to fetch licenses!")
    #     flash('Unable to fetch licenses!')
    context.update(
        {
            "pagination": {},  # TODO
            "api_base_url": os.environ["SHELF_API_EXTERNAL_BASE_URL"],
        }
    )

    return render_page("apps/shelf/licenses/many.html", context=context)


@blueprint.route("/data", methods=["GET"])
def get_licenses_data():
    """Get all licenses data."""
    context = get_context()
    current_app.logger.debug("context: %s", context)
    api_client = current_app.config[constants.SWEETRPG_API_CLIENT_KEY]
    try:
        # url = os.environ[constants.SHELF_API_BASE_URL]
        # current_app.logger.debug("(SHELF_API_BASE_URL) url: %s", url)
        licenses = api_client.query(LICENSE)
        # context.update({'licenses': licenses})
        return licenses
    except:
        current_app.logger.exception("Unable to fetch licenses!")
        # flash('Unable to fetch licenses!')
        return []


@blueprint.route("/<id>", methods=["GET"])
def get_license_page(id: str):
    """Get a specific license page."""
    context = get_context()
    current_app.logger.debug("context: %s", context)
    # api_client = current_app.config[constants.SWEETRPG_API_CLIENT_KEY]
    # try:
    #     license = api_client.get(LICENSE, id)
    #     context.update({'license': license})
    # except:
    #     current_app.logger.exception(f"Unable to fetch license {id}!")
    #     flash(f'Unable to fetch license {id}!')
    context.update({"id": id})

    return render_page("apps/shelf/licenses/detail.html", context=context)


@blueprint.route("/<id>/data", methods=["GET"])
def get_license_data(id: str):
    """Get a specific license data."""
    context = get_context()
    current_app.logger.debug("context: %s", context)
    api_client = current_app.config[constants.SWEETRPG_API_CLIENT_KEY]
    try:
        license = api_client.get(LICENSE, id)
        # context.update({'license': license})
        return license
    except:
        current_app.logger.exception(f"Unable to fetch license {id}!")
        # flash(f'Unable to fetch license {id}!')
        raise NotFound(f"Unable to fetch license {id}!")
