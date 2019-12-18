__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
game_systems.py
- Game Systems API
"""


from flask import session, jsonify, request, current_app
from application.blueprints.api import blueprint
from application import constants
from application.models import constants as model_constants
from application.models.common.game_system import GameSystem, GameSystemFacetDatum, GameSystemImageDatum
from application.models.entitlement import Entitlement, EntitlementGrant
from application.blueprints.api import user_required, user_optional
from application.db import db


@blueprint.route('/gamesystems', methods=['GET'])
@user_optional
def all_game_systems(current_user):
    current_app.logger.debug(f"GET /gamesystems: {request}")
    game_systems = GameSystem.query.all()
    current_app.logger.debug(f"game_systems: {game_systems}")

    ordered_game_systems = []
    unordered_game_systems = []
    for gs in game_systems:
        if current_user:
            grant = EntitlementGrant.for_user(current_user, model_constants.ENTITLEMENT_GAME_SYSTEMS)
            if grant:
                gs.locked = False
            else:
                continue
        elif gs.locked:
            continue

        if gs.order is None:
            unordered_game_systems.append(gs)
        else:
            ordered_game_systems.append(gs)

    ordered_game_systems.sort(key=lambda gs: gs.order)
    unordered_game_systems.sort(key=lambda gs: gs.name)

    game_systems = [gs.to_dict() for gs in (ordered_game_systems + unordered_game_systems)]

    return {
        'game_systems': game_systems,
    }


@blueprint.route('/gamesystems/<key>', methods=['GET'])
def game_system_by_key(key):
    current_app.logger.debug(f"GET /gamesystems/<key>: {request}")
    game_system = GameSystem.query.filter_by(key=key).first()
    current_app.logger.debug(f"game_system: {game_system}")
    return game_system.to_dict()
