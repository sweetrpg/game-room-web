# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from flask import current_app
from flask_rest_jsonapi import ResourceList, ResourceDetail, ResourceRelationship
from .schema import PersonAPISchema
from sweetrpg_library_model.model.person import Person
from sweetrpg_api_core.data import APIData
from sweetrpg_game_room_web.application.db import db
from sweetrpg_game_room_web.application.blueprints.setup import model_info
from sweetrpg_game_room_web.application.auth import oauth


class PersonList(ResourceList):
    disable_oauth = True
    schema = PersonAPISchema
    data_layer = {"class": APIData, "type": "person", "model": Person, "db": db, "model_info": model_info}

    @oauth.require_oauth('create_person')
    def post(*args, **kwargs):
        current_app.logger.debug("args: %s, kwargs: %s", args, kwargs)
        return "TODO"


class PersonDetail(ResourceDetail):
    disable_oauth = True
    schema = PersonAPISchema
    data_layer = {"class": APIData, "type": "person", "model": Person, "db": db, "model_info": model_info}

    @oauth.require_oauth('update_person')
    def patch(*args, **kwargs):
        current_app.logger.debug("args: %s, kwargs: %s", args, kwargs)
        return "TODO"

    @oauth.require_oauth('delete_person')
    def delete(*args, **kwargs):
        current_app.logger.debug("args: %s, kwargs: %s", args, kwargs)
        return "TODO"


class PersonVolumeRelationship(ResourceRelationship):
    disable_oauth = True
    schema = PersonAPISchema
    data_layer = {"class": APIData, "type": "person", "model": Person, "db": db, "model_info": model_info}
