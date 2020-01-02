__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
user.py
- Utility functions for managing users.
"""


from flask import current_app
from application.db import db
from application.models.user import User, Identity, Role, UserRole
from application.models import constants as model_constants
import hashlib


def has_role(user: User, role_name: str):
    for role_assoc in user.roles:
        if role_assoc.enabled and role_assoc.roles.name == role_name:
            return True

    return False


def create_or_add_user(userinfo: dict, role_name: str = model_constants.ROLE_USER):
    email = userinfo['email']
    subject = userinfo['sub']

    # find the role
    role = Role.query.filter_by(name=role_name).first()
    if not role:
        current_app.logger.error(f"Role {role_name} not found!")
        return None, None

    # find the user object
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        user.nickname = userinfo['nickname']
        user.name = userinfo['name']
        if userinfo.get('picture'):
            current_app.logger.info("Using provided picture URL for avatar.")
            user.avatar_url = userinfo['picture']
        else:
            current_app.logger.info("Calculating hash for gravatar...")
            canonical_email = email.strip().lower()
            email_hash = hashlib.md5(canonical_email).hexdigest()
            current_app.logger.debug(f"email_hash: {email_hash}")
            user.avatar_url = f'https://www.gravatar.com/avatar/{email_hash}?s=30'

        db.session.add(user)
        db.session.commit()

        role_assoc = UserRole(user, role)
        db.session.add(role_assoc)
        db.session.commit()
    print(user)

    # find identity object
    identity = Identity.query.filter_by(subject=subject).first()
    if not identity:
        source = subject.split('|', 2)[0]
        identity = Identity(user=user, source=source, subject=subject)
        # TODO

        db.session.add(identity)
        db.session.commit()
    print(identity)

    return user, identity
