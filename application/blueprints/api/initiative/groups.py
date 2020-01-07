__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
groups.py
- Groups API
"""


from flask import session, jsonify, request, current_app
from application.blueprints.api import blueprint
from application import constants
from application.models import constants as model_constants
from application.models.initiative.participant import Participant, ParticipantGroup
from application.blueprints.api import user_required
from application.db import db
from application.blueprints.api.validators import validate_payload, validate_user, check_dependent_object
from application.blueprints.api.initiative.validators import CreateGroupInput
from application.blueprints.api.exceptions import error_response
from application.utils import normalize_query
from werkzeug.exceptions import Forbidden, BadRequest, NotFound
from datetime import datetime


@blueprint.route('/groups', methods=['GET'])
@user_required
def get_groups(current_user):
    current_app.logger.debug(f"GET /groups: {request}, current_user: {current_user}")
    user_id = current_user.id
    groups = ParticipantGroup.query.filter_by(creator_id=user_id).all()
    current_app.logger.debug(f"groups: {groups}")
    return {
        'groups': [e.to_dict() for e in groups],
    }


@blueprint.route('/groups/<int:group_id>', methods=['GET'])
@user_required
def get_group(current_user, group_id: int):
    current_app.logger.debug(f"GET /groups/{group_id}: {request}, current_user: {current_user}, group_id: {group_id}")
    user_id = current_user.id
    current_app.logger.debug(f"user_id: {user_id}")
    group = ParticipantGroup.query.filter_by(id=group_id).first()
    validate_user(group, current_user)
    current_app.logger.debug(f"group_id: {group_id}")
    return group.to_dict()



@blueprint.route('/groups', methods=['POST'])
@user_required
def create_group(current_user):
    current_app.logger.debug(f"POST /groups: {request}, current_user: {current_user}")

    validate_payload(CreateGroupInput, request)

    data = request.get_json()
    current_app.logger.debug(f"data: {data}")

    name = data['name']

    group = ParticipantGroup(name)
    group.creator_id = current_user.id

    db.session.add(group)
    db.session.commit()

    return jsonify(group.to_dict()), 201
