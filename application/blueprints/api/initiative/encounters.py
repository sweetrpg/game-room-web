__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
encounters.py
- Encounters API
"""


from flask import session, jsonify, request, current_app
from application.blueprints.api import blueprint
from application import constants
from application.models import constants as model_constants
from application.models.initiative.tracked_encounter import TrackedEncounter
from application.models.initiative.encounter import Encounter, EncounterParticipant, EncounterSession
from application.models.initiative.participant import Participant, ParticipantGroup
from application.models.common.game_system import GameSystem
from application.blueprints.api import user_required
from application.db import db
from application.blueprints.api.validators import validate_payload, validate_user, check_dependent_object
from application.blueprints.api.initiative.validators import CreateEncounterInput, UpdateEncounterInput, AddParticipantInput, UpdateParticipantInput, UpdateSessionInput, UpdateParticipantOrderInput
from application.blueprints.api.exceptions import error_response
from application.controllers.encounter import EncounterController
from werkzeug.exceptions import Forbidden, BadRequest, NotFound
from datetime import datetime


@blueprint.route('/encounters', methods=['GET'])
@user_required
def get_encounters(current_user):
    current_app.logger.debug(f"GET /encounters: {request}, current_user: {current_user}")
    user_id = current_user.id
    encounters = TrackedEncounter.query.filter_by(creator_id=user_id).all()
    current_app.logger.debug(f"encounters: {encounters}")
    return {
        'encounters': [e.to_dict() for e in encounters],
    }


@blueprint.route('/encounters/<int:encounter_id>', methods=['GET'])
@user_required
def get_encounter(current_user, encounter_id: int):
    current_app.logger.debug(f"GET /encounters/{encounter_id}: {request}, current_user: {current_user}, encounter_id: {encounter_id}")
    user_id = current_user.id
    current_app.logger.debug(f"user_id: {user_id}")
    encounter = TrackedEncounter.query.filter_by(id=encounter_id).first()
    validate_user(encounter, current_user)
    current_app.logger.debug(f"encounter: {encounter}")
    return encounter.to_dict()


@blueprint.route('/encounters/<int:encounter_id>/next', methods=['POST'])
@user_required
def next_participant(current_user, encounter_id: int):
    current_app.logger.debug(f"GET /encounters/{encounter_id}/next: {request}, current_user: {current_user}, encounter_id: {encounter_id}")
    user_id = current_user.id
    current_app.logger.debug(f"user_id: {user_id}")
    tracked_encounter = TrackedEncounter.query.filter_by(id=encounter_id).first()
    validate_user(tracked_encounter, current_user)
    current_app.logger.debug(f"tracked_encounter: {tracked_encounter}")

    controller = EncounterController(encounter_id)
    next_participant_index = controller.get_next_index()
    current_app.logger.debug(f"next_participant_index: {next_participant_index}")
    if next_participant_index is not None:
        participant = controller[next_participant_index]
        current_app.logger.info(f"participant: {participant}")
        if participant:
            return jsonify({ 'index': next_participant_index, 'participant': participant.to_dict() })

    return jsonify({ 'index': -1, 'participant': {} })


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
    check_dependent_object(game_system, 'gameSystem')

    encounter = Encounter(name=name, game_system=game_system)
    theme = data.get('theme')
    if theme:
        encounter.flags = [f'theme:{theme}']
    encounter.creator_id = current_user.id

    db.session.add(encounter)
    db.session.commit()

    group = ParticipantGroup(name=name)
    group.creator_id = current_user.id
    group.flags = [model_constants.FLAG_TRACKED_ENCOUNTER]
    db.session.add(group)
    db.session.commit()

    session = EncounterSession(start_date=datetime.utcnow(), encounter=encounter)
    session.flags = [model_constants.FLAG_TRACKED_ENCOUNTER]
    session.creator_id = current_user.id

    db.session.add(session)
    db.session.commit()

    te = TrackedEncounter(group=group, encounter=encounter, session=session)
    te.tie_breaker = data.get('tieBreaker') or model_constants.ENUM_TIE_BREAKER_QUERY
    te.ordering = data.get('ordering') or model_constants.ENUM_ORDERING_HIGH_TO_LOW
    te.creator_id = current_user.id

    db.session.add(te)
    db.session.commit()

    return jsonify(te.to_dict()), 201


@blueprint.route('/encounters/<int:encounter_id>', methods=['PUT'])
@user_required
def update_encounter(current_user, encounter_id: int):
    current_app.logger.debug(
        f"PUT /encounters/{encounter_id}: {request}, current_user: {current_user}")

    validate_payload(UpdateEncounterInput, request)

    data = request.get_json()
    current_app.logger.debug(f"data: {data}")

    tracked_encounter = TrackedEncounter.query.filter_by(id=encounter_id).first()
    current_app.logger.debug(f"tracked_encounter: {tracked_encounter}")
    validate_user(tracked_encounter, current_user)

    encounter = Encounter.query.filter_by(id=tracked_encounter.encounter_id).first()
    current_app.logger.debug(f"encounter: {encounter}")
    validate_user(encounter, current_user)

    for k, v in data.items():
        current_app.logger.debug(f"{k}={v}")
        setattr(encounter, k, v)

    db.session.add(encounter)
    db.session.commit()

    return jsonify(encounter.to_dict())


@blueprint.route('/encounters/<int:encounter_id>/participants', methods=['POST'])
@user_required
def add_participants(current_user, encounter_id: int):
    current_app.logger.debug(f"POST /encounters/{encounter_id}/participants: {request}, current_user: {current_user}")

    validate_payload(AddParticipantInput, request)

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
                             f"'quantity' value of '{quantity}' is outside of range (1-100)", 'quantity')

    # check encounter
    tracked_encounter = TrackedEncounter.query.filter_by(id=encounter_id).first()
    current_app.logger.debug(f"tracked_encounter: {tracked_encounter}")
    validate_user(tracked_encounter, current_user)

    encounter = Encounter.query.filter_by(id=tracked_encounter.encounter_id).first()
    current_app.logger.debug(f"encounter: {encounter}")
    validate_user(encounter, current_user)

    created_participants = []
    created_encounter_participants = []

    # TODO: find name of existing group for encounter
    pg = ParticipantGroup.query.filter_by(id=tracked_encounter.group_id).first()
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

    position_offset = len(encounter.participants)

    for i,p in enumerate(created_participants):
        ep = EncounterParticipant(participant=p, encounter=encounter)
        ep.creator_id = current_user.id
        ep.position = i + position_offset
        ep.order = i + position_offset
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
    current_app.logger.debug(f"PUT /encounters/{encounter_id}/participants/{participant_id}: {request}, current_user: {current_user}")

    # validate payload
    data = request.get_json()
    current_app.logger.debug(f"data: {data}")

    validate_payload(UpdateParticipantInput, request)

    # check encounter
    tracked_encounter = TrackedEncounter.query.filter_by(id=encounter_id).first()
    current_app.logger.debug(f"tracked_encounter: {tracked_encounter}")
    validate_user(tracked_encounter, current_user)

    encounter = Encounter.query.filter_by(id=tracked_encounter.encounter_id).first()
    current_app.logger.debug(f"encounter: {encounter}")
    validate_user(encounter, current_user)

    # check participant
    encounter_participant = EncounterParticipant.query.filter_by(id=participant_id).first()
    current_app.logger.debug(f"encounter_participant: {encounter_participant}")
    validate_user(encounter_participant, current_user)

    participant = Participant.query.filter_by(id=encounter_participant.participant_id).first()
    current_app.logger.debug(f"participant: {participant}")
    validate_user(participant, current_user)

    for k,v in data.items():
        current_app.logger.debug(f"{k}={v}")
        setattr(encounter_participant, k, v)
        setattr(participant, k, v)

    current_app.logger.debug(f"encounter_participant: {encounter_participant}")
    current_app.logger.debug(f"participant: {participant}")

    db.session.add(encounter_participant)
    db.session.add(participant)
    db.session.commit()

    return jsonify(participant.to_dict())


@blueprint.route('/encounters/<int:encounter_id>/participants/<int:participant_id>', methods=['DELETE'])
@user_required
def delete_participant(current_user, encounter_id: int, participant_id: int):
    current_app.logger.debug(
        f"DELETE /encounters/{encounter_id}/participants/{participant_id}: {request}, current_user: {current_user}")

    # check encounter
    tracked_encounter = TrackedEncounter.query.filter_by(id=encounter_id).first()
    current_app.logger.debug(f"tracked_encounter: {tracked_encounter}")
    validate_user(tracked_encounter, current_user)

    encounter = Encounter.query.filter_by(id=tracked_encounter.encounter_id).first()
    current_app.logger.debug(f"encounter: {encounter}")
    validate_user(encounter, current_user)

    # check participant
    encounter_participant = EncounterParticipant.query.filter_by(id=participant_id).first()
    current_app.logger.debug(f"encounter_participant: {encounter_participant}")
    validate_user(encounter_participant, current_user)

    participant = Participant.query.filter_by(id=encounter_participant.participant_id).first()
    current_app.logger.debug(f"participant: {participant}")
    validate_user(participant, current_user)

    db.session.delete(encounter_participant)
    db.session.delete(participant)
    db.session.commit()

    return jsonify({}), 204


@blueprint.route('/encounters/<int:encounter_id>/participants', methods=['DELETE'])
@user_required
def delete_participants(current_user, encounter_id: int):
    current_app.logger.debug(f"DELETE /encounters/{encounter_id}/participants: {request}, current_user: {current_user}")

    # check encounter
    tracked_encounter = TrackedEncounter.query.filter_by(id=encounter_id).first()
    current_app.logger.debug(f"tracked_encounter: {tracked_encounter}")
    validate_user(tracked_encounter, current_user)

    encounter = Encounter.query.filter_by(id=tracked_encounter.encounter_id).first()
    current_app.logger.debug(f"encounter: {encounter}")
    validate_user(encounter, current_user)

    encounter_participants = EncounterParticipant.query.filter_by(encounter_id=encounter.id).all()

    types = request.args.get('types')
    current_app.logger.debug(f"types: {types}")

    for ep in encounter_participants:
        current_app.logger.debug(f"encounter_participant: {ep}")
        validate_user(ep, current_user)

        participant = Participant.query.filter_by(id=ep.participant_id).first()
        validate_user(participant, current_user)

        if types is None or participant.type in types:
            current_app.logger.info(f"Participant's type matches or requsted type is empty; deleting.")
            db.session.delete(ep)
            db.session.delete(participant)

    db.session.commit()

    return jsonify({}), 204


@blueprint.route('/encounters/<int:encounter_id>/participants/reset', methods=['POST'])
@user_required
def reset_participants(current_user, encounter_id: int):
    current_app.logger.debug(f"POST /encounters/{encounter_id}/participants/reset: {request}, current_user: {current_user}")

    # check encounter
    tracked_encounter = TrackedEncounter.query.filter_by(id=encounter_id).first()
    current_app.logger.debug(f"tracked_encounter: {tracked_encounter}")
    validate_user(tracked_encounter, current_user)

    encounter = Encounter.query.filter_by(id=tracked_encounter.encounter_id).first()
    current_app.logger.debug(f"encounter: {encounter}")
    validate_user(encounter, current_user)

    encounter_participants = EncounterParticipant.query.filter_by(encounter_id=encounter.id).all()

    types = request.args.get('types')
    current_app.logger.debug(f"types: {types}")

    for ep in encounter_participants:
        current_app.logger.debug(f"encounter_participant: {ep}")
        validate_user(ep, current_user)

        participant = Participant.query.filter_by(id=ep.participant_id).first()
        validate_user(participant, current_user)

        ep.order = 0

        db.session.add(ep)

    db.session.commit()

    return jsonify({}), 204


@blueprint.route('/encounters/<int:encounter_id>/session', methods=['PUT'])
@user_required
def update_session(current_user, encounter_id: int):
    current_app.logger.debug(f"PUT /encounters/{encounter_id}/session: {request}, current_user: {current_user}")

    data = request.get_json()
    current_app.logger.debug(f"data: {data}")

    validate_payload(UpdateSessionInput, request)

    # check encounter
    tracked_encounter = TrackedEncounter.query.filter_by(id=encounter_id).first()
    current_app.logger.debug(f"tracked_encounter: {tracked_encounter}")
    validate_user(tracked_encounter, current_user)

    session = EncounterSession.query.filter_by(id=tracked_encounter.session_id).first()
    current_app.logger.debug(f"session: {session}")
    validate_user(session, current_user)

    for k, v in data.items():
        current_app.logger.debug(f"{k}={v}")
        setattr(session, k, v)

    current_app.logger.debug(f"session: {session}")

    db.session.add(session)
    db.session.commit()

    return jsonify(session.to_dict())


@blueprint.route('/encounters/<int:encounter_id>/order', methods=['PUT'])
@user_required
def update_participant_order(current_user, encounter_id: int):
    current_app.logger.debug(
        f"PUT /encounters/{encounter_id}/order: {request}, current_user: {current_user}")

    data = request.get_json()
    current_app.logger.debug(f"data: {data}")

    validate_payload(UpdateParticipantOrderInput, request)

    # check encounter
    tracked_encounter = TrackedEncounter.query.filter_by(
        id=encounter_id).first()
    current_app.logger.debug(f"tracked_encounter: {tracked_encounter}")
    validate_user(tracked_encounter, current_user)

    session = EncounterSession.query.filter_by(id=tracked_encounter.session_id).first()
    current_app.logger.debug(f"session: {session}")
    validate_user(session, current_user)

    for participant_id, value in data.items():
        current_app.logger.debug(f"{participant_id}={value}")

        participant = EncounterParticipant.query.filter_by(id=int(participant_id)).first()
        participant.order = int(value)

        db.session.add(participant)
    #     setattr(session, k, v)

    # session.turn_queue = []
    # current_app.logger.debug(f"session: {session}")

    # db.session.add(session)
    db.session.commit()

    # TODO: do ordering according to encounter controller
    controller = EncounterController(encounter_id)
    controller.sort_participants()
    controller.set_turn_to(0)

    encounter = Encounter.query.filter_by(id=tracked_encounter.encounter_id).first()

    return jsonify(encounter.to_dict())
