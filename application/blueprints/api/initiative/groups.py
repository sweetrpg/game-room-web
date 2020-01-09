__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
groups.py
- Groups API
"""


from flask import session, jsonify, request, current_app
from application.blueprints.api import blueprint
from application import constants
from application.models import constants as model_constants
from application.models.initiative.tracked_encounter import TrackedEncounter
from application.models.initiative.encounter import Encounter
from application.models.initiative.participant import Participant, ParticipantGroup, ParticipantHealthDatum
from application.blueprints.api import user_required
from application.db import db
from application.blueprints.api.validators import validate_payload, validate_user, check_dependent_object
from application.blueprints.api.initiative.validators import CreateGroupInput, AddGroupParticipantInput
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

    group = ParticipantGroup(name=name)
    group.creator_id = current_user.id

    db.session.add(group)
    db.session.commit()

    return jsonify(group.to_dict()), 201


@blueprint.route('/groups/<int:group_id>/participants', methods=['POST'])
@user_required
def add_group_participants(current_user, group_id: int):
    current_app.logger.debug(f"POST /groups/{group_id}/participants: {request}, current_user: {current_user}")

    validate_payload(AddGroupParticipantInput, request)

    # validate payload
    data = request.get_json()
    current_app.logger.debug(f"data: {data}")

    name = data['name']
    current_app.logger.debug(f"name: {name}")
    participant_type = data['type']
    quantity = int(data.get('quantity')) or 1
    current_app.logger.debug(f"quantity: {quantity}")
    if quantity < 1 or quantity > 100:
        raise error_response(BadRequest, 'invalid_value',
                             f"'quantity' value of '{quantity}' is outside of range (1-100)",
                             'quantity')

    # check group
    pg = ParticipantGroup.query.filter_by(id=group_id).first()
    current_app.logger.debug(f"participant_group: {pg}")
    validate_user(pg, current_user)

    created_participants = []

    for i in range(quantity):
        current_app.logger.debug(f"i: {i}")
        participant_name = name
        if quantity > 1:
            participant_name = f"{name} {i + 1}"
        current_app.logger.debug(f"participant_name: {participant_name}")

        p = Participant(name=participant_name, group=pg)
        p.creator_id = current_user.id
        p.participant_type = participant_type
        db.session.add(p)
        current_app.logger.debug(f"p: {p}")

        created_participants.append(p)

    current_app.logger.info("Committing participants...")
    db.session.commit()
    current_app.logger.info("Committed.")

    response = {
        'participant_ids': [p.id for p in created_participants]
    }

    return jsonify(response), 201


@blueprint.route('/groups/from/<int:encounter_id>', methods=['POST'])
@user_required
def create_group_from_encounter(current_user, encounter_id: int):
    current_app.logger.debug(f"POST /groups/from/{encounter_id}: {request}, current_user: {current_user}")
    user_id = current_user.id
    current_app.logger.debug(f"user_id: {user_id}")

    tracked_encounter = TrackedEncounter.query.filter_by(id=encounter_id).first()
    current_app.logger.debug(f"tracked_encounter: {tracked_encounter}")
    validate_user(tracked_encounter, current_user)

    encounter = Encounter.query.filter_by(id=tracked_encounter.encounter_id).first()
    current_app.logger.debug(f"encounter: {encounter}")
    validate_user(encounter, current_user)

    group = ParticipantGroup.query.filter_by(id=tracked_encounter.group_id).first()
    current_app.logger.debug(f"group: {group}")
    validate_user(group, current_user)

    pg = ParticipantGroup(name=group.name)
    pg.creator_id = current_user.id

    db.session.add(pg)
    db.session.commit()

    for participant in group.participants:
        p = Participant(name=participant.name,
                        participant_type=participant.participant_type,
                        group=pg)
        db.session.add(p)
        db.session.commit()

        for health_data in participant.health_data:
            phd = ParticipantHealthDatum(key=health_data.key, value=health_data.value,
                                         participant=p)
            db.session.add(phd)

        db.session.commit()

    return jsonify(pg.to_dict()), 201
