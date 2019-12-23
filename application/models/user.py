__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
user.py
- User model object
"""

from datetime import datetime
from application.db import db
from sqlalchemy.dialects.postgresql import ENUM
from application.models import constants as model_constants


class User(db.Model):
    """
    An object that represents a single person in the system. A User can have multiple
    identities, each stemming from an authentication source.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    nickname = db.Column(db.String(30), nullable=True)
    name = db.Column(db.String(120), nullable=True)
    avatar_url = db.Column(db.String(1024), nullable=True)

    def __init__(self, email):
        self.email = email

    def to_dict(self):
        return dict(id=self.id,
                    email=self.email,
                    nickname=self.nickname,
                    name=self.name,
                    avatar_url=self.avatar_url)


class Identity(db.Model):
    """
    A login identity, from a particular source.
    """
    __tablename__ = 'identities'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    source = db.Column(ENUM(model_constants.ENUM_IDENTITY_SOURCE_AMAZON,
                            model_constants.ENUM_IDENTITY_SOURCE_GITHUB,
                            model_constants.ENUM_IDENTITY_SOURCE_GOOGLE,
                            model_constants.ENUM_IDENTITY_SOURCE_LINKEDIN,
                            model_constants.ENUM_IDENTITY_SOURCE_TWITTER,
                            model_constants.ENUM_IDENTITY_SOURCE_WORDPRESS,
                            model_constants.ENUM_IDENTITY_SOURCE_SMS,
                            model_constants.ENUM_IDENTITY_SOURCE_EMAIL,
                            model_constants.ENUM_IDENTITY_SOURCE_DB,
                            model_constants.ENUM_IDENTITY_SOURCE_SYSTEM,
                            name='identity_source'),
                       nullable=False)
    subject = db.Column(db.String(100), nullable=False) # the ID from the source auth

    def __init__(self, user, source, subject):
        self.user_id = user.id
        self.source = source
        self.subject = subject

    def to_dict(self):
        return dict(id=self.id,
                    user_id=self.user_id,
                    source=self.source,
                    subject=self.subject)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return dict(id=self.id,
                    name=self.name)
