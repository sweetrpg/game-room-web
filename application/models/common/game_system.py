__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
game_system.py
- Game system related objects.
"""

from datetime import datetime
from application.db import db


class GameSystem(db.Model):
    __tablename__ = 'game_systems'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    key = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    edition = db.Column(db.String(20), nullable=True)
    details = db.Column(db.Text, nullable=True)
    facets = db.Column(db.PickleType, nullable=True)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return dict(id=self.id,
                    key=self.key,
                    name=self.name,
                    full_name=self.full_name,
                    edition=self.edition,
                    details=self.details,
                    facets=self.facets,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'))


class GameSystemImageDatum(db.Model):
    __tablename__ = 'game_system_image_data'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    name = db.Column(db.String(50), nullable=False)
    scale = db.Column(db.Float, nullable=False)
    data = db.Column(db.PickleType, nullable=False)
    game_system_id = db.Column(db.Integer, db.ForeignKey('game_systems.id'))

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return dict(id=self.id,
                    name=self.name,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'))


class GameSystemFacetDatum(db.Model):
    __tablename__ = 'game_system_facet_data'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    details = db.Column(db.Text, nullable=False)
    facet = db.Column(db.String(50), nullable=False)
    label = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    source = db.Column(db.String(1024), nullable=False)
    game_system_id = db.Column(db.Integer, db.ForeignKey('game_systems.id'))
    # images = db.relationship('GameSystemImageDatum', backref='f')
    items = db.Column(db.PickleType, nullable=False)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return dict(id=self.id,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    details=self.details,
                    facet=self.facet,
                    label=self.label,
                    name=self.name,
                    source=self.source,
                    # images=[image.to_dict() for image in self.images],
                    items=self.items)


class GameSystemImageSet(object):
    # TODO: dynamically load a set of images
    pass
