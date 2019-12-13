__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
profile.py
- User profile model object
"""

from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
from ..db import db


class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data = db.Column(db.PickleType, nullable=False, default='{}')
    # TODO

    def __init__(self, user):
        self.user_id = user.id

    def to_dict(self):
        return dict(id=self.id,
                    user_id=self.user_id,
                    data=self.data)
