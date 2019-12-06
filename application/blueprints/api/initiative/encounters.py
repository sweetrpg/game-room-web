__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
encounters.py
- Encounters API
"""


from flask import session, jsonify, request, current_app
from application.blueprints.api import blueprint
from application import constants
from application.models.initiative.encounter import Encounter
from application.models.common.game_system import GameSystem
from application.blueprints.api import user_required
from application.db import db
from werkzeug.exceptions import Forbidden


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

    data = request.get_json()
    current_app.logger.debug(f"data: {data}")

    name = data.get('name')
    if not name:
        return {'error': "'name' not provided"}, 400
    game_system_key = data.get('gameSystem')
    if not game_system_key:
        return {
            'code': 'missing_attribute',
            'attribute': 'gameSystem',
            'message': "'gameSystem' not provided",
            }, 400

    game_system = GameSystem.query.filter_by(key=game_system_key).first()
    if not game_system:
        return {'error': f"Game system '{game_system_key}' not found'"}, 400

    encounter = Encounter(name=name, game_system=game_system)
    encounter.ordering = data.get('ordering') or 'high-to-low'
    # TODO: theme as a flag value
    encounter.creator_id = current_user.id

    db.session.add(encounter)
    db.session.commit()

    return jsonify(encounter.to_dict()), 201
