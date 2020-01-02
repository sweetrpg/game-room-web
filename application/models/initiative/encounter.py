__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
encounter.py
- Encounter model objects.
"""

from datetime import datetime
from application.db import db
from application.models.user import User
from application.models.common.game_system import GameSystem
from .participant import Participant
from .group import EncounterGroup
from sqlalchemy.dialects.postgresql import ENUM
from flask import current_app


class Encounter(db.Model):
    __tablename__ = 'encounters'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    name = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(40), nullable=True)
    flags = db.Column(db.PickleType, nullable=True, default=[])
    game_system_id = db.Column(db.Integer, db.ForeignKey('game_systems.id'))
    participants = db.relationship('EncounterParticipant', backref='encounters', lazy=False)
    # maps = db.relationship('Map')

    def __init__(self, name:str, game_system:GameSystem):
        self.name = name
        self.game_system_id = game_system.id

    def to_dict(self):
        creator = User.query.filter_by(id=self.creator_id).first()
        game_system = GameSystem.query.filter_by(id=self.game_system_id).first()

        self.participants.sort(key=lambda x: x.position)
        current_app.logger.debug(f"participants: {self.participants}")

        return dict(id=self.id,
                    creator=creator.to_dict(),
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    name=self.name,
                    notes=self.notes,
                    category=self.category,
                    flags=list(set(self.flags)),
                    game_system=game_system.to_dict(),
                    participants=[p.to_dict() for p in self.participants])
                    # TODO: map_ids=[m.id for m in self.maps])


class EncounterParticipant(db.Model):
    __tablename__ = 'encounter_participants'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'))
    color = db.Column(db.String(10), nullable=True)
    # conditions = db.Column(db.String(50), nullable=False)
    encounter_id = db.Column(db.Integer, db.ForeignKey('encounters.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('participant_groups.id'), nullable=True)
    marker = db.Column(db.String(10), nullable=False, default="")
    order = db.Column(db.Integer, nullable=False, default=0) # the displayed value
    position = db.Column(db.Integer, nullable=False, default=0) # the actual position in the list
    size = db.Column(db.Float, nullable=False, default=1)
    flags = db.Column(db.PickleType, nullable=True, default=[])
    tag = db.Column(db.String(10), nullable=False, default="")
    notes = db.Column(db.Text, nullable=True)
    # target_ids = db.Column(db.String(50), nullable=False)
    x = db.Column(db.Float, nullable=False, default=0)
    y = db.Column(db.Float, nullable=False, default=0)
    z = db.Column(db.Float, nullable=False, default=0)
    layer = db.Column(ENUM('normal', 'background', 'secret', 'always', name='encounter_participant_layer'),
                      nullable=False, default="normal")
    hidden = db.Column(db.Boolean, nullable=False, default=False)
    scale = db.Column(db.Float, nullable=False, default=1)

    def __init__(self, participant:Participant, encounter:Encounter, group:EncounterGroup = None):
        self.participant_id = participant.id
        self.encounter_id = encounter.id
        if group:
            self.group_id = group.id

    def to_dict(self):
        p = Participant.query.filter_by(id=self.participant_id).first()

        return dict(id=self.id,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    participant=p.to_dict(),
                    color=self.color,
                    encounter_id=self.encounter_id,
                    group_id=self.group_id,
                    marker=self.marker,
                    order=self.order,
                    size=self.size,
                    flags=list(set(self.flags)),
                    tag=self.tag,
                    notes=self.notes,
                    x=self.x, y=self.y, z=self.z,
                    layer=self.layer,
                    hidden=self.hidden,
                    scale=self.scale)


class EncounterParticipantGroup(db.Model):
    __tablename__ = 'encounter_participant_groups'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    name = db.Column(db.String(50), nullable=False)
    flags = db.Column(db.PickleType, nullable=True, default=[])
    encounter_id = db.Column(db.Integer, db.ForeignKey('encounters.id'))

    def __init__(self, name:str, encounter:Encounter):
        self.name = name
        self.encounter_id = encounter.id

    def to_dict(self):
        return dict(id=self.id,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    name=self.gameSystem,
                    encounter_id=self.encounter_id)


class EncounterParticipantHealthDatum(db.Model):
    __tablename__ = 'encounter_participant_health_data'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    key = db.Column(db.String(20), nullable=False)
    value = db.Column(db.String(50), nullable=False)
    encounter_participant_id = db.Column(db.Integer, db.ForeignKey('encounter_participants.id'))

    def __init__(self, key:str, value:str, participant:EncounterParticipant):
        self.key = key
        self.value = value
        self.encounter_participant_id = participant.id

    def to_dict(self):
        return dict(id=self.id,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    key=self.key,
                    value=self.value,
                    encounter_participant_id=self.encounter_participant_id)


class EncounterParticipantMetrics(db.Model):
    __tablename__ = 'encounter_participant_metrics'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    turn_count = db.Column(db.Integer, nullable=False, default=0)
    average_turn_length = db.Column(db.Float, nullable=False, default=0)
    longest_turn_length = db.Column(db.Float, nullable=False, default=0)
    shortest_turn_length = db.Column(db.Float, nullable=False, default=0)
    encounter_participant_id = db.Column(db.Integer, db.ForeignKey('encounter_participants.id'))

    def __init__(self, participant:EncounterParticipant):
        self.encounter_participant_id = participant.id

    def to_dict(self):
        return dict(id=self.id,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    turn_count=self.turn_count,
                    average_turn_length=self.average_turn_length,
                    longest_turn_length=self.longest_turn_length,
                    shortest_turn_length=self.shortest_turn_length,
                    encounter_participant_id=self.encounter_participant_id)


class EncounterParticipantTurnData(db.Model):
    __tablename__ = 'encounter_participant_turn_data'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    turn_count = db.Column(db.Integer, nullable=False, default=1)
    turns_taken = db.Column(db.Integer, nullable=False, default=0)
    encounter_participant_id = db.Column(db.Integer, db.ForeignKey('encounter_participants.id'))

    def __init__(self, participant: EncounterParticipant):
        self.encounter_participant_id = participant.id

    def to_dict(self):
        return dict(id=self.id,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    turn_count=self.turn_count,
                    turns_taken=self.turns_taken,
                    encounter_participant_id=self.encounter_participant_id)


class EncounterRegion(db.Model):
    __tablename__ = 'encounter_regions'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    color = db.Column(db.String(10), nullable=True)
    # conditions = db.relationship('Condition', backref='region', lazy=False)
    flags = db.Column(db.PickleType, nullable=True, default=[])
    encounter_id = db.Column(db.Integer, db.ForeignKey('encounters.id'))
    encounter_participant_id = db.Column(db.Integer, db.ForeignKey('encounter_participants.id'), nullable=True)
    name = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    height = db.Column(db.Float, nullable=False, default=1)
    width = db.Column(db.Float, nullable=False, default=1)
    x = db.Column(db.Float, nullable=False, default=0)
    y = db.Column(db.Float, nullable=False, default=0)
    layer = db.Column(ENUM('normal', 'background', 'secret', 'always', name='encounter_region_layer'),
                      nullable=False, default='normal')
    hidden = db.Column(db.Boolean, nullable=False, default=False)
    scale = db.Column(db.Float, nullable=False, default=1)

    def __init__(self, name:str, encounter: Encounter):
        self.name = name
        self.encounter_id = encounter.id

    def to_dict(self):
        return dict(id=self.id,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    color=self.color,
                    flags=list(set(self.flags)),
                    encounter_id=self.encounter_id,
                    encounter_participant_id=self.encounter_participant_id,
                    name=self.name,
                    notes=self.notes,
                    height=self.height,
                    width=self.width,
                    x=self.x,
                    y=self.y,
                    layer=self.layer,
                    hidden=self.hidden,
                    scale=self.scale)


class EncounterSession(db.Model):
    __tablename__ = 'encounter_sessions'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    name = db.Column(db.String(50), nullable=True)
    current_participant_index = db.Column(db.Integer, nullable=True)
    current_round = db.Column(db.Integer, nullable=False, default=0)
    end_date = db.Column(db.DateTime, nullable=True)
    number_of_rounds = db.Column(db.Integer, nullable=False, default=0)
    number_of_turns = db.Column(db.Integer, nullable=False, default=0)
    start_date = db.Column(db.DateTime, nullable=False)
    flags = db.Column(db.PickleType, nullable=True, default=[])
    turn_queue = db.Column(db.PickleType, nullable=False, default=[])
    encounter_id = db.Column(db.Integer, db.ForeignKey('encounters.id'))

    def __init__(self, start_date: datetime, encounter: Encounter):
        self.start_date = start_date
        self.encounter_id = encounter.id

    def to_dict(self):
        return dict(id=self.id,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    name=self.name,
                    current_participant_index=self.current_participant_index,
                    current_round=self.current_round,
                    end_date=self.end_date.strftime('%Y-%m-%d %H:%M:%S') if self.end_date else None,
                    number_of_rounds=self.number_of_rounds,
                    number_of_turns=self.number_of_turns,
                    start_date=self.start_date.strftime('%Y-%m-%d %H:%M:%S'),
                    flags=list(set(self.flags)),
                    turn_queue=str(self.turn_queue),
                    encounter_id=self.encounter_id)


class EncounterSessionTimelineEntry(db.Model):
    __tablename__ = 'encounter_session_timeline_entries'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    details = db.Column(db.Text, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('encounter_sessions.id'))
    ended = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    encounter_participant_id = db.Column(db.Integer, db.ForeignKey('encounter_participants.id'))
    round = db.Column(db.String(50), nullable=False, default=1)
    started = db.Column(db.DateTime, default=datetime.utcnow)
    # TODO: target_ids = db.Column(db.String(50), nullable=False)

    def __init__(self, session):
        self.session_id = session.id

    def to_dict(self):
        return dict(id=self.id,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    details=self.details,
                    session_id=self.session_id,
                    ended=self.ended.strftime('%Y-%m-%d %H:%M:%S'),
                    notes=self.notes,
                    encounter_participant_id=self.encounter_participant_id,
                    round=self.round,
                    started=self.started.strftime('%Y-%m-%d %H:%M:%S'))
