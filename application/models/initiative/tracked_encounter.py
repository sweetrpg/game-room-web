__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
tracked_encounter.py
- Encounter meta model objects.
"""

from datetime import datetime
from application.db import db
from application.models.user import User
from application.models.common.game_system import GameSystem
from .participant import ParticipantGroup
from .encounter import Encounter, EncounterSession
from application.models import constants
from sqlalchemy.dialects.postgresql import ENUM


class TrackedEncounter(db.Model):
    __tablename__ = 'tracked_encounters'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    group_id = db.Column(db.Integer, db.ForeignKey('participant_groups.id'))
    encounter_id = db.Column(db.Integer, db.ForeignKey('encounters.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('encounter_sessions.id'))
    ordering = db.Column(ENUM(constants.ENUM_ORDERING_HIGH_TO_LOW,
                              constants.ENUM_ORDERING_LOW_TO_HIGH,
                              constants.ENUM_ORDERING_PCVADVERSARY,
                              constants.ENUM_ORDERING_PLAYER_MANAGED,
                              name='encounter_ordering'),
                         nullable=False, default=constants.ENUM_ORDERING_HIGH_TO_LOW)
    tie_breaker = db.Column(ENUM(constants.ENUM_TIE_BREAKER_ALPHA,
                                 constants.ENUM_TIE_BREAKER_QUERY,
                                 constants.ENUM_TIE_BREAKER_RANDOM,
                                 name='encounter_tie_breaker'),
                         nullable=False, default=constants.ENUM_TIE_BREAKER_QUERY)

    def __init__(self, group: ParticipantGroup, encounter: Encounter, session: EncounterSession):
        self.group_id = group.id
        self.encounter_id = encounter.id
        self.session_id = session.id

    def to_dict(self):
        creator = User.query.filter_by(id=self.creator_id).first()

        group = ParticipantGroup.query.filter_by(id=self.group_id).first()
        encounter = Encounter.query.filter_by(id=self.encounter_id).first()
        session = EncounterSession.query.filter_by(id=self.session_id).first()

        return dict(id=self.id,
                    creator=creator.to_dict(),
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    ordering=self.ordering,
                    tie_breaker=self.tie_breaker,
                    group=group.to_dict(),
                    encounter=encounter.to_dict(),
                    session=session.to_dict())
