# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

import functools
# from flask_rest_jsonapi import Api
from .manager import TagList, TagDetail
from ...blueprints import api


def setup_routes(app):
    # app.logger.info("Registering tag models...")
    # for model_name, model_info in tag_model_info.items():
    #     APIData.add_model(model_name, model_info)

    app.logger.info("Setting up routes for Tags API")
    # api = Api(app)
    api.route(TagList, "tag_list", "/tags/")
    api.route(TagDetail, "tag_detail", "/tags/<id>")
    # api.route(TagAuthorRelationship, "tag_authors", "/tags/<id>/relationships/authors")
