# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from flask_rest_jsonapi import ResourceList, ResourceDetail, ResourceRelationship
from .schema import PublisherAPISchema
from sweetrpg_api_core.data import APIData
from sweetrpg_library_model.model.publisher import Publisher
from sweetrpg_library_web.application.db import db
from sweetrpg_library_web.application.blueprints.setup import model_info


class PublisherList(ResourceList):
    schema = PublisherAPISchema
    data_layer = {"class": APIData, "type": "publisher", "model": Publisher, "db": db, "model_info": model_info}


class PublisherDetail(ResourceDetail):
    schema = PublisherAPISchema
    data_layer = {
        "class": APIData,
        "type": "publisher",
        "model": Publisher,
        "db": db,
        "model_info": model_info
    }


# class PublisherAuthorRelationship(ResourceRelationship):
#     schema = PublisherAPISchema
#     data_layer = {
#         "class": APIData,
#         "type": "publisher",
#         "model": Publisher,
#         "db": db,
#         "model_info": model_info
#     }
