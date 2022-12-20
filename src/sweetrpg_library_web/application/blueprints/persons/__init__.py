# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Person routes.
"""

import functools
from flask import Blueprint, current_app, render_template, request, g, flash
from sweetrpg_library_web.application import constants
from sweetrpg_web_core.helpers.context import get_context
from sweetrpg_client.types import PERSON
from sweetrpg_client.exceptions import NotFound
import os
from sweetrpg_library_web.application.blueprints import render_page


blueprint = Blueprint("persons", __name__, url_prefix="/persons")


@blueprint.route("/", methods=["GET"])
def get_persons_page():
    """Get all persons page.

    """
    context = get_context()
    current_app.logger.debug("context: %s", context)
    # api_client = current_app.config[constants.SWEETRPG_API_CLIENT_KEY]
    # try:
    #     # url = os.environ[constants.LIBRARY_API_BASE_URL]
    #     # current_app.logger.debug("(LIBRARY_API_BASE_URL) url: %s", url)
    #     persons = api_client.query(PERSON)
    #     context.update({'persons': persons})
    # except:
    #     current_app.logger.exception("Unable to fetch persons!")
    #     flash('Unable to fetch persons!')
    context.update({
                    'pagination': {},  # TODO
                    'api_base_url': os.environ['LIBRARY_API_EXTERNAL_BASE_URL'],
                    })

    return render_page("apps/library/persons/many.html", context=context)
