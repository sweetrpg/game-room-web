# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Table routes.
"""

from flask import Blueprint, current_app, request, flash
from flask_babel import gettext as _
from sweetrpg_game_room_web.application import constants
from sweetrpg_web_core.helpers.context import get_context
from sweetrpg_game_room_web.application.blueprints import render_page, local_redirect


blueprint = Blueprint("tables", __name__, url_prefix="/tables")


def _client():
    return current_app.config[constants.GAME_ROOM_CLIENT_KEY]


def _catalog():
    return current_app.config[constants.CATALOG_CLIENT_KEY]


@blueprint.route("/", methods=["GET"])
def get_tables_page():
    """List the current user's tables."""
    context = get_context()
    user_id = context["user"]["id"]
    if not user_id:
        context.update({"tables": [], "is_owner": True})
        return render_page("apps/game-room/tables/collection.html", context=context)
    return _render_tables_list(context, user_id)


@blueprint.route("/users/<user_id>", methods=["GET"])
def get_user_tables_page(user_id: str):
    """View another user's tables, filtered by game-room-api to what the viewer may see."""
    context = get_context()
    return _render_tables_list(context, user_id)


def _render_tables_list(context: dict, user_id: str):
    tables = []
    try:
        tables = _client().list_tables(user_id) or []
    except Exception:
        current_app.logger.exception("Unable to list tables for user %s!", user_id)
        flash(_("Unable to load these tables right now."))
    context.update(
        {
            "tables": tables,
            "is_owner": context["user"]["id"] == user_id,
            "tables_owner_id": user_id,
        }
    )
    return render_page("apps/game-room/tables/collection.html", context=context)


@blueprint.route("/new", methods=["GET"])
def new_table_page():
    """Show the create-table form. Visibility defaults to private."""
    context = get_context()
    context.update({"visibility_levels": constants.VISIBILITY_LEVELS, "default_visibility": "private"})
    return render_page("apps/game-room/tables/form.html", context=context)


@blueprint.route("/", methods=["POST"])
def create_table():
    """Create a table. Visibility defaults to private if not supplied."""
    context = get_context()
    user_id = context["user"]["id"]
    name = request.form.get("name", "").strip()
    visibility = request.form.get("visibility") or "private"
    if not name:
        flash(_("A table name is required."))
        return local_redirect("web.tables.new_table_page")
    try:
        table = _client().create_table(user_id, name, visibility)
        return local_redirect("web.tables.get_table_page", id=table["id"])
    except Exception:
        current_app.logger.exception("Unable to create table %r for user %s!", name, user_id)
        flash(_("Unable to create that table right now."))
        return local_redirect("web.tables.new_table_page")


@blueprint.route("/<id>", methods=["GET"])
def get_table_page(id: str):
    """Show a table's detail: its volumes and visibility (current user's own table)."""
    context = get_context()
    return _render_table(context, context["user"]["id"], id)


@blueprint.route("/users/<user_id>/<id>", methods=["GET"])
def get_user_table_page(user_id: str, id: str):
    """View another user's table, filtered by game-room-api to what the viewer may see."""
    context = get_context()
    return _render_table(context, user_id, id)


def _render_table(context: dict, owner_id: str, id: str):
    table = None
    try:
        table = _client().get_table(owner_id, id)
    except Exception:
        current_app.logger.exception("Unable to fetch table %s for user %s!", id, owner_id)
        flash(_("Unable to load that table right now."))
    volume_titles = {}
    if table and table.get("volume_ids"):
        try:
            volume_titles = _catalog().titles_for(table["volume_ids"])
        except Exception:
            current_app.logger.exception("Unable to resolve volume titles for table %s!", id)
    context.update(
        {
            "table": table,
            "is_owner": context["user"]["id"] == owner_id,
            "visibility_levels": constants.VISIBILITY_LEVELS,
            "volume_titles": volume_titles,
        }
    )
    return render_page("apps/game-room/tables/detail.html", context=context)


@blueprint.route("/<id>", methods=["POST"])
def update_table(id: str):
    """Update a table's name/visibility, or delete it."""
    context = get_context()
    user_id = context["user"]["id"]
    if request.form.get("_method") == "DELETE":
        try:
            _client().delete_table(user_id, id)
            flash(_("Table deleted."))
        except Exception:
            current_app.logger.exception("Unable to delete table %s for user %s!", id, user_id)
            flash(_("Unable to delete that table right now."))
        return local_redirect("web.tables.get_tables_page")

    # The detail page saves name and visibility independently (instant edit, no Save button),
    # so a POST may carry only one field. Fall back to the current value for whatever is absent.
    current = {}
    try:
        current = _client().get_table(user_id, id) or {}
    except Exception:
        current_app.logger.exception("Unable to fetch table %s before update!", id)

    name = request.form.get("name")
    name = name.strip() if name is not None else (current.get("name") or "")
    visibility = request.form.get("visibility") or current.get("visibility") or "private"
    if not name:
        flash(_("A table name is required."))
        return local_redirect("web.tables.get_table_page", id=id)
    try:
        _client().update_table(user_id, id, name, visibility)
        flash(_("Table updated."))
    except Exception:
        current_app.logger.exception("Unable to update table %s for user %s!", id, user_id)
        flash(_("Unable to update that table right now."))
    return local_redirect("web.tables.get_table_page", id=id)


@blueprint.route("/<id>/volumes", methods=["POST"])
def add_volume(id: str):
    """Add a volume to a table."""
    context = get_context()
    user_id = context["user"]["id"]
    volume_id = request.form.get("volume_id", "").strip()
    if volume_id:
        try:
            _client().add_table_volume(user_id, id, volume_id)
        except Exception:
            current_app.logger.exception("Unable to add volume %s to table %s!", volume_id, id)
            flash(_("Unable to add that volume right now."))
    return local_redirect("web.tables.get_table_page", id=id)


@blueprint.route("/<id>/volumes/<volume_id>", methods=["POST"])
def remove_volume(id: str, volume_id: str):
    """Remove a volume from a table."""
    context = get_context()
    user_id = context["user"]["id"]
    if request.form.get("_method") == "DELETE":
        try:
            _client().remove_table_volume(user_id, id, volume_id)
        except Exception:
            current_app.logger.exception("Unable to remove volume %s from table %s!", volume_id, id)
            flash(_("Unable to remove that volume right now."))
    return local_redirect("web.tables.get_table_page", id=id)
