# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from sweetrpg_library_model.model.author import Author
from sweetrpg_library_model.db.author.document import AuthorDocument
from sweetrpg_library_model.model.volume import Volume
from sweetrpg_library_model.db.volume.document import VolumeDocument
from sweetrpg_library_model.model.publisher import Publisher
from sweetrpg_library_model.db.publisher.document import PublisherDocument
from sweetrpg_library_model.model.review import Review
from sweetrpg_library_model.db.review.document import ReviewDocument
from sweetrpg_library_model.model.system import System
from sweetrpg_library_model.db.system.document import SystemDocument
from sweetrpg_library_model.model.studio import Studio
from sweetrpg_library_model.db.studio.document import StudioDocument
from sweetrpg_library_model.model.tag import Tag
from sweetrpg_library_model.db.tag.document import TagDocument
from sweetrpg_library_model.model.volume_property import VolumeProperty
from sweetrpg_library_model.db.volume_property.document import VolumePropertyDocument


model_info = {
    "author": {
        "model": Author,
        # "schema": AuthorSchema,
        "document": AuthorDocument,
        "type": "author",
        "collection": "authors",
        "properties": {"volumes": "volume"},
    },
    "volume": {
        "model": Volume,
        # "schema": VolumeSchema,
        "document": VolumeDocument,
        "type": "volume",
        "collection": "volumes",
        "properties": {"authors": "author", "properties": "volume_property"},
    },
    "publisher": {
        "model": Publisher,
        # "schema": PublisherSchema,
        "document": PublisherDocument,
        "type": "publisher",
        "collection": "publishers",
        "properties": {},
    },
    "review": {
        "model": Review,
        # "schema": ReviewSchema,
        "document": ReviewDocument,
        "type": "review",
        "collection": "reviews",
        "properties": {"volumes": "volume"},
    },
    "studio": {
        "model": Studio,
        # "schema": StudioSchema,
        "document": StudioDocument,
        "type": "studio",
        "collection": "studios",
        "properties": {"authors": "author"},
    },
    "system": {
        "model": System,
        # "schema": SystemSchema,
        "document": SystemDocument,
        "type": "system",
        "collection": "systems",
        "properties": {},
    },
    "tag": {
        "model": Tag,
        # "schema": TagSchema,
        "document": TagDocument,
        "type": "tag",
        "collection": "tags",
        "properties": {},
    },
    "volume_property": {
        "model": VolumeProperty,
        # "schema": VolumePropertySchema,
        "document": VolumePropertyDocument,
        "type": "volume_property",
        "collection": "volume_properties",
        "properties": {"volumes": "volume"},
    },
}
