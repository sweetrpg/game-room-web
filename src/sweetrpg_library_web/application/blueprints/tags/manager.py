# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from flask_rest_jsonapi import ResourceList, ResourceDetail, ResourceRelationship
from .schema import TagAPISchema
from sweetrpg_api_core.data import APIData
from sweetrpg_library_model.model.tag import Tag
from sweetrpg_library_web.application.db import db
from sweetrpg_library_web.application.blueprints.setup import model_info


class TagList(ResourceList):
    schema = TagAPISchema
    data_layer = {"class": APIData, "type": "tag", "model": Tag, "db": db, "model_info": model_info}


class TagDetail(ResourceDetail):
    schema = TagAPISchema
    data_layer = {
        "class": APIData,
        "type": "tag",
        "model": Tag,
        "db": db,
        "model_info": model_info
    }


# class TagAuthorRelationship(ResourceRelationship):
#     schema = TagAPISchema
#     data_layer = {
#         "class": APIData,
#         "type": "tag",
#         "model": Tag,
#         "db": db,
#         "model_info": model_info
#     }
