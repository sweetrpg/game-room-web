__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
encounters.py
- Encounters API
"""


from flask import session, jsonify, request, current_app
from application.blueprints.api import blueprint
from application import constants
from application.models.initiative.encounter import Encounter, EncounterParticipant
from application.models.initiative.participant import Participant, ParticipantGroup
from application.models.common.game_system import GameSystem
from application.blueprints.api import user_required
from application.db import db
from application.blueprints.api.validators import validate_payload
from application.blueprints.api.initiative.validators import CreateEncounterInput
from werkzeug.exceptions import Forbidden, BadRequest, NotFound
from ..exceptions import error_response


@blueprint.route('/encounters', methods=['GET'])
@user_required
def get_encounters(current_user):
    current_app.logger.debug(f"GET /encounters: {request}, current_user: {current_user}")
    user_id = current_user.id
    current_app.logger.debug(f"user_id: {user_id}")
    encounters = Encounter.query.filter_by(creator_id=user_id)
    current_app.logger.debug(f"encounters: {encounters}")
    return {
        'encounters': [e.to_dict() for e in encounters],
    }


@blueprint.route('/encounters/<int:encounter_id>', methods=['GET'])
@user_required
def get_encounter(current_user, encounter_id: int):
    current_app.logger.debug(f"GET /encounters: {request}, current_user: {current_user}, encounter_id: {encounter_id}")
    user_id = current_user.id
    current_app.logger.debug(f"user_id: {user_id}")
    encounter = Encounter.query.filter_by(id=encounter_id).first()
    if encounter.creator_id != user_id:
        raise Forbidden("You are not allowed to access this encounter")
    current_app.logger.debug(f"encounter: {encounter}")
    return {
        'encounter': encounter.to_dict(),
    }


@blueprint.route('/encounters', methods=['POST'])
@user_required
def create_encounter(current_user):
    current_app.logger.debug(f"POST /encounters: {request}, current_user: {current_user}")

    validate_payload(CreateEncounterInput, request)

    data = request.get_json()
    current_app.logger.debug(f"data: {data}")

    name = data['name']
    game_system_key = data['gameSystem']

    game_system = GameSystem.query.filter_by(key=game_system_key).first()
    if not game_system:
        raise error_response(BadRequest, 'object_not_found',
                             f"Game system '{game_system_key}' not found", 'gameSystem')

    encounter = Encounter(name=name, game_system=game_system)
    encounter.ordering = data.get('ordering') or 'high-to-low'
    # TODO: theme as a flag value
    encounter.creator_id = current_user.id

    db.session.add(encounter)
    db.session.commit()

    return jsonify(encounter.to_dict()), 201


@blueprint.route('/encounters/<int:encounter_id>', methods=['PUT'])
@user_required
def update_encounter(current_user, encounter_id: int):
    # TODO
    pass


@blueprint.route('/encounters/<int:encounter_id>/participants', methods=['POST'])
@user_required
def add_participants(current_user, encounter_id: int):
    current_app.logger.debug(f"POST /encounters/{encounter_id}/participants: {request}, current_user: {current_user}")

    # validate payload
    data = request.get_json()
    current_app.logger.debug(f"data: {data}")
    name = data.get('name')
    current_app.logger.debug(f"name: {name}")
    if not name or len(name) == 0:
        return {
            'code': 'missing_attribute',
            'attribute': 'name',
            'message': "'name' not provided or empty in payload"
        }, 400
    participant_type = data.get('type')
    current_app.logger.debug(f"participant_type: {participant_type}")
    if not participant_type or len(participant_type) == 0:
        return {
            'code': 'missing_attribute',
            'attribute': 'type',
            'message': "'type' not provided or empty in payload"
        }, 400
    if participant_type not in ['pc', 'adversary', 'object']:
        return {
            'code': 'invalid_value',
            'attribute': 'type',
            'message': f"'type' value of '{participant_type}' is not valid"
        }, 400
    quantity = data.get('quantity')
    current_app.logger.debug(f"quantity: {quantity}")
    if not quantity or not isinstance(quantity, int):
        return {
            'code': 'missing_attribute',
            'attribute': 'quantity',
            'message': "'quantity' not provided or empty in payload"
        }, 400
    if quantity < 1 or quantity > 100:
        return {
            'code': 'invalid_value',
            'attribute': 'quantity',
            'message': f"'quantity' value of '{quantity}' is outside of range (1-100)"
        }, 400

    # check encounter
    encounter = Encounter.query.filter_by(id=encounter_id).first()
    current_app.logger.debug(f"encounter: {encounter}")
    if not encounter:
        return {
            'code': 'no_encounter',
            'attribute': None,
            'message': f"Encounter '{encounter_id}' not found"
        }, 400
    if encounter.creator_id != current_user.id:
        return {
            'code': 'forbidden',
            'attribute': None,
            'message': "You are not allowed to modify this encounter"
        }, 403

    created_participants = []
    created_encounter_participants = []

    # TODO: find name of existing group for encounter
    pg = ParticipantGroup(name="group")
    pg.creator_id = current_user.id
    pg.flags = ['encounter']
    db.session.add(pg)
    current_app.logger.info("Committing participant group...")
    db.session.commit()
    current_app.logger.info("Committed.")

    current_app.logger.debug(f"pg: {pg}")

    for i in range(quantity):
        current_app.logger.debug(f"i: {i}")
        participant_name = name
        if quantity > 1:
            participant_name = f"{name} {i + 1}"
        current_app.logger.debug(f"participant_name: {participant_name}")

        p = Participant(name=participant_name, group_id=pg.id)
        p.creator_id = current_user.id
        p.participant_type = participant_type
        db.session.add(p)
        current_app.logger.debug(f"p: {p}")

        created_participants.append(p)

    current_app.logger.info("Committing participants...")
    db.session.commit()
    current_app.logger.info("Committed.")

    for p in created_participants:
        ep = EncounterParticipant(participant=p, encounter=encounter)
        ep.creator_id = current_user.id
        db.session.add(ep)
        current_app.logger.debug(f"ep: {ep}")

        created_encounter_participants.append(ep)

    current_app.logger.debug(f"created_participants: {created_participants}")

    current_app.logger.info("Committing encounter participants...")
    db.session.commit()
    current_app.logger.info("Committed.")

    response = {
        'participant_ids': [ep.id for ep in created_participants]
    }

    return jsonify(response), 201


@blueprint.route('/encounters/<int:encounter_id>/participants/<int:participant_id>', methods=['PUT'])
@user_required
def update_participant(current_user, encounter_id: int, participant_id: int):
    current_app.logger.debug(f"POST /encounters/{encounter_id}/participants/{participant_id}: {request}, current_user: {current_user}")

    # validate payload
    data = request.get_json()
    current_app.logger.debug(f"data: {data}")

    # check encounter
    encounter = Encounter.query.filter_by(id=encounter_id).first()
    current_app.logger.debug(f"encounter: {encounter}")
    if not encounter:
        return {
            'code': 'no_encounter',
            'attribute': None,
            'message': f"Encounter '{encounter_id}' not found"
        }, 400
    if encounter.creator_id != current_user.id:
        return {
            'code': 'forbidden',
            'attribute': None,
            'message': "You are not allowed to modify this participant"
        }, 403

    # check participant
    encounter_participant = EncounterParticipant.query.filter_by(id=participant_id).first()
    current_app.logger.debug(f"encounter_participant: {encounter_participant}")
    if not encounter_participant:
        raise error_response(BadRequest, 'no_encounter_participant', f"Participant '{participant_id}' not found")
    if encounter_participant.creator_id != current_user.id:
        raise error_response(Forbidden, 'forbidden', "You are not allowed to modify this participant")

    participant = Participant.query.filter_by(id=encounter_participant.participant.id).first()
    current_app.logger.debug(f"participant: {participant}")
    if not participant:
        raise error_response(BadRequest, 'no_participant', f'Participant for {encounter_participant.participant.id} not found', 'participant.id')

    for k,v in data.items():
        current_app.logger.debug(f"{k}={v}")
        setattr(encounter_participant, k, v)
        setattr(participant, k, v)

    current_app.logger.debug(f"encounter_participant: {encounter_participant}")
    current_app.logger.debug(f"participant: {participant}")

    db.session.add(encounter_participant)
    db.session.add(participant)
    db.session.commit()

    return participant.to_dict(), 204
