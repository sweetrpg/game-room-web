__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
from ..db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    identity_id = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    nickname = db.Column(db.String(30), nullable=True)
    name = db.Column(db.String(120), nullable=True)
    avatar_url = db.Column(db.String(1024), nullable=True)

    def __init__(self, identity_id, email):
        self.email = email
        self.identity_id = identity_id
        # self.password = generate_password_hash(password, method='sha256')

    # @classmethod
    # def authenticate(cls, **kwargs):
    #     email = kwargs.get('email')
    #     # password = kwargs.get('password')

    #     if not email or not password:
    #         return None

    #     user = cls.query.filter_by(email=email).first()
    #     if not user or not check_password_hash(user.password, password):
    #         return None

    #     return user

    def to_dict(self):
        return dict(id=self.id,
                    identity_id=self.identity_id,
                    email=self.email,
                    nickname=self.nickname,
                    name=self.name,
                    avatar_url=self.avatar_url)
