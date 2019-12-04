__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
turn_queue.py
- Non-model objects for turn queue.
"""

from datetime import datetime
from application.db import db
import enum


class TurnQueueType(enum.Enum):
    participant = 'participant'
    group = 'group'
    placeholder = 'placeholder'


class TurnQueueID(object):
    turn_queue_type = ""
    identifier = ""

    def __init__(self, turn_queue_type: TurnQueueType = None, identifier: str = None, spec: str = None):
        if spec:
            self.turn_queue_type = 'TODO'
            self.identifier = 'TODO'
        else:
            self.turn_queue_type = turn_queue_type
            self.identifier = identifier

    def to_uri(self):
        pass

    def to_dict(self):
        return dict(turn_queue_type=self.turn_queue_type,
                    identifier=self.identifier)
