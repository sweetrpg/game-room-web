__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
game_systems.py
- Game Systems API
"""


from flask import session, jsonify, request, current_app
from application.blueprints.api import blueprint
from application import constants
from application.models.common.game_system import GameSystem, GameSystemFacetDatum, GameSystemImageDatum
from application.blueprints.api import user_required
from application.db import db


@blueprint.route('/gamesystems', methods=['GET'])
def all_game_systems():
    current_app.logger.debug(f"GET /gamesystems: {request}")
    game_systems = GameSystem.query.all()
    current_app.logger.debug(f"game_systems: {game_systems}")
    return {
        'game_systems': [gs.to_dict() for gs in game_systems],
    }


@blueprint.route('/gamesystems/<key>', methods=['GET'])
def game_system_by_key(key):
    current_app.logger.debug(f"GET /gamesystems/<key>: {request}")
    game_system = GameSystem.query.filter_by(key=key).first()
    current_app.logger.debug(f"game_system: {game_system}")
    return game_system.to_dict()
