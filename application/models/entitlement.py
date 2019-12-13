__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
entitlement.py
- User entitlements model object
"""

from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
from ..db import db


class Entitlement(db.Model):
    __tablename__ = 'entitlements'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    # TODO

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return dict(id=self.id,
                    name=self.name)


class EntitlementGrant(db.Model):
    __tablename__ = 'entitlement_grants'

    id = db.Column(db.Integer, primary_key=True)
    entitlement_id = db.Column(db.Integer, db.ForeignKey('entitlements.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # TODO

    def __init__(self, user, entitlement):
        self.user_id = user.id
        self.entitlement_id = entitlement.id

    @staticmethod
    def for_user(user, entitlement_name):
        entitlement = Entitlement.query.filter_by(name=entitlement_name).first()
        if entitlement:
            grant = EntitlementGrant.query.filter_by(user_id=user.id, entitlement_id=entitlement.id).first()
            return grant

        return None

    def to_dict(self):
        user = User.query.filter_by(id=self.user_id).first()
        entitlement = Entitlement.query.filter_by(id=self.entitlement_id).first()

        return dict(id=self.id,
                    entitlement=entitlement.to_dict(),
                    user=user.to_dict())
