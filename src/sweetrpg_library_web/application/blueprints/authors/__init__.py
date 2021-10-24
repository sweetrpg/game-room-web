# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

import functools
from flask_rest_jsonapi import Api
from .manager import AuthorList, AuthorDetail, AuthorVolumeRelationship
from ...blueprints import api


def setup_routes(app):
    # app.logger.info("Registering author models...")
    # for model_name, model_info in author_model_info.items():
    #     APIData.add_model(model_name, model_info)

    app.logger.info("Setting up routes for Authors API")
    # api = Api(app)
    api.route(AuthorList, "author_list", "/authors/")
    api.route(AuthorDetail, "author_detail", "/authors/<id>")
    api.route(AuthorVolumeRelationship, "author_volumes", "/authors/<id>/relationships/volumes")
