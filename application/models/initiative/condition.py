__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
condition.py
- Condition related objects.
"""

from datetime import datetime
from application.db import db
from sqlalchemy.dialects.postgresql import ENUM


class Condition(db.Model):
    __tablename__ = 'conditions'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    end_type = db.Column(ENUM('save', 'startOfTurn', 'endOfTurn', 'encounter', 'region', 'fixed', name='condition_end_type'),
                         nullable=False, default='save')
    end_value = db.Column(db.String(20), nullable=True)
    flags = db.Column(db.PickleType, nullable=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.PickleType, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    source = db.Column(ENUM('me', 'participant', 'region', 'gameSystem', name='condition_source'),
                       nullable=False, default='me')
    condition_type = db.Column(ENUM('normal', 'ongoing', 'custom', name='condition_type'),
                               nullable=False, default='normal')

    def __init__(self, name:str, condition_type:str):
        self.name = name
        self.condition_type = condition_type

    def to_dict(self):
        return dict(id=self.id,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    name=self.name,
                    flags=set(self.flags),
                    end_type=self.end_type,
                    end_value=self.end_value,
                    image=None, # TODO
                    notes=self.notes,
                    source=self.source,
                    type=self.condition_type)


class ConditionHealthAdjustment(db.Model):
    __tablename__ = 'condition_health_adjustments'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    health_key = db.Column(db.String(20), nullable=False)
    adjustment = db.Column(db.String(20), nullable=True)
    condition_id = db.Column(db.String(50), nullable=False)


    def __init__(self, condition:Condition, key:str, adjustment:str):
        self.condition_id = condition.id
        self.health_key = key
        self.adjustment = adjustment

    def to_dict(self):
        return dict(id=self.id,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    condition_id=self.condition_id,
                    health_key=self.health_key,
                    adjustment=self.adjustment)
