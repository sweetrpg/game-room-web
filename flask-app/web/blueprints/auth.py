"""
auth.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""

from functools import wraps
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, current_app
import jwt
from web.db import db
from web.models.user import User
import constants


auth_blueprint = Blueprint('auth', __name__)



def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated


# def token_required(f):
#     @wraps(f)
#     def _verify(*args, **kwargs):
#         auth_headers = request.headers.get('Authorization', '').split()

#         invalid_msg = {
#             'message': 'Invalid token. Registeration and / or authentication required',
#             'authenticated': False
#         }
#         expired_msg = {
#             'message': 'Expired token. Reauthentication required.',
#             'authenticated': False
#         }

#         if len(auth_headers) != 2:
#             return jsonify(invalid_msg), 401

#         try:
#             token = auth_headers[1]
#             data = jwt.decode(token, current_app.config['SECRET_KEY'])
#             user = User.query.filter_by(email=data['sub']).first()
#             if not user:
#                 raise RuntimeError("User not found")
#             return f(user, *args, **kwargs)
#         except jwt.ExpiredSignatureError:
#             return jsonify(expired_msg), 401
#         except (jwt.InvalidTokenError, Exception) as e:
#             print(e)
#             return jsonify(invalid_msg), 401

#     return _verify



@auth_blueprint.route('/callback')
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session[constants.JWT_PAYLOAD] = userinfo
    session[constants.PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')


@auth_blueprint.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


@auth_blueprint.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))
