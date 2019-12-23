__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
user.py
- Utility functions for managing users.
"""


from application.db import db
from application.models.user import User, Identity


def create_or_add_user(userinfo: dict):
    email = userinfo['email']
    subject = userinfo['sub']

    # find the user object
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        user.nickname = userinfo['nickname']
        user.name = userinfo['name']
        if userinfo.get('picture'):
            user.avatar_url = userinfo['picture']
        else:
            user.avatar_url = 'https://www.gravatar.com/avatar/#(gravatarHash)?s=30'

        db.session.add(user)
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
