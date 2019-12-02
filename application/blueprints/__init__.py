__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""


from functools import wraps
from flask import redirect, session, render_template
from application import constants


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return redirect('/auth/login')
        return f(*args, **kwargs)

    return decorated


# def user_info(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         if constants.PROFILE_KEY in session:
#             kwargs.update({
#                 'userinfo': session[constants.PROFILE_KEY],
#             })
#         return f(*args, **kwargs)

#     return decorated

def render_page(page, context={}):
    userinfo = session.get(constants.PROFILE_KEY)
    if userinfo:
        context.update({
            'userinfo': userinfo,
        })
    print(f"context: {context}")

    return render_template(page, **context)
