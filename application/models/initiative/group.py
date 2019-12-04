__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
group.py
- Encounter group model objects.
"""


from datetime import datetime
from application.db import db


class EncounterGroup(db.Model):
    __tablename__ = 'encounter_groups'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    name = db.Column(db.String(50), nullable=False)
    flags = db.Column(db.PickleType, nullable=True)
    # encounters = db.relationship('Encounter', backref='group', lazy=False)

    def __init__(self, name:str):
        self.name = name

    def to_dict(self):
        return dict(id=self.id,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    name=self.name,
                    flags=self.flags)
                    # encounter_ids=[e.id for e in self.encounters])
