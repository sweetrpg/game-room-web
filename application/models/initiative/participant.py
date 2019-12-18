__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
participant.py
- Participant model objects.
"""

from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
from application.db import db
from sqlalchemy.dialects.postgresql import ENUM
import uuid


class Participant(db.Model):
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    name = db.Column(db.String(50), nullable=False)
    participant_type = db.Column(ENUM('pc', 'adversary', 'object', name='participant_type'),
                                 nullable=False)
    flags = db.Column(db.PickleType, nullable=True, default=[])
    color = db.Column(db.String(20), nullable=True)
    # conditions = db.relationship('Condition', backref='participant')
    external_key = db.Column(db.String(1024), nullable=True)
    guid = db.Column(db.String(32), nullable=False, default=uuid.uuid4().hex)
    image = db.Column(db.PickleType, nullable=True)
    marker = db.Column(db.String(20), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    size = db.Column(db.Integer, nullable=False, default=1)
    group_id = db.Column(db.Integer, db.ForeignKey('participant_groups.id'))
    health_data = db.relationship('ParticipantHealthDatum', backref='participant')

    def __init__(self, name, group_id):
        self.name = name
        self.group_id = group_id

    def to_dict(self):
        return dict(id=self.id,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    name=self.name,
                    type=self.participant_type,
                    flags=set(self.flags),
                    color=self.color,
                    external_key=self.external_key,
                    guid=self.guid,
                    image=self.image,
                    marker=self.marker,
                    notes=self.notes,
                    size=self.size,
                    group_id=self.group_id,
                    health_data=[hd for hd in self.health_data])


class ParticipantGroup(db.Model):
    __tablename__ = 'participant_groups'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    name = db.Column(db.String(50), nullable=False)
    flags = db.Column(db.PickleType, nullable=True, default=[])
    participants = db.relationship('Participant', backref='group', lazy=False)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return dict(id=self.id,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    name=self.name,
                    flags=set(self.flags),
                    participants=[p.to_dict() for p in self.participants])


class ParticipantHealthDatum(db.Model):
    __tablename__ = 'participant_health_data'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    key = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(50), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'))

    def __init__(self, key, value, participant):
        self.key = key
        self.value = value
        self.participant_id = participant.id

    def to_dict(self):
        return dict(id=self.id,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    key=self.key,
                    value=self.value,
                    participant_id=self.participant_id)
