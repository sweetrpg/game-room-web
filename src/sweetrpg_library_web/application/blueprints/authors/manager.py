# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from flask import current_app
from flask_rest_jsonapi import ResourceList, ResourceDetail, ResourceRelationship
from .schema import AuthorAPISchema
from sweetrpg_library_model.model.author import Author
from sweetrpg_api_core.data import APIData
from sweetrpg_library_web.application.db import db
from sweetrpg_library_web.application.blueprints.setup import model_info
from sweetrpg_library_web.application.auth import oauth


class AuthorList(ResourceList):
    disable_oauth = True
    schema = AuthorAPISchema
    data_layer = {"class": APIData, "type": "author", "model": Author, "db": db, "model_info": model_info}

    @oauth.require_oauth('create_author')
    def post(*args, **kwargs):
        current_app.logger.debug("args: %s, kwargs: %s", args, kwargs)
        return "TODO"


class AuthorDetail(ResourceDetail):
    disable_oauth = True
    schema = AuthorAPISchema
    data_layer = {"class": APIData, "type": "author", "model": Author, "db": db, "model_info": model_info}

    @oauth.require_oauth('update_author')
    def patch(*args, **kwargs):
        current_app.logger.debug("args: %s, kwargs: %s", args, kwargs)
        return "TODO"

    @oauth.require_oauth('delete_author')
    def delete(*args, **kwargs):
        current_app.logger.debug("args: %s, kwargs: %s", args, kwargs)
        return "TODO"


class AuthorVolumeRelationship(ResourceRelationship):
    disable_oauth = True
    schema = AuthorAPISchema
    data_layer = {"class": APIData, "type": "author", "model": Author, "db": db, "model_info": model_info}
