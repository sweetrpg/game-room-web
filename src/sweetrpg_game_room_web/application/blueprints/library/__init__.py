# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Library routes.
"""

from flask import Blueprint, current_app, request, jsonify, flash, redirect, url_for
from sweetrpg_game_room_web.application import constants
from sweetrpg_web_core.helpers.context import get_context
from sweetrpg_game_room_web.application.blueprints import render_page


blueprint = Blueprint("library", __name__, url_prefix="/library")


def _client():
    return current_app.config[constants.SHELF_CLIENT_KEY]


@blueprint.route("/", methods=["GET"])
def get_library_page():
    """Get the current user's library page."""
    context = get_context()
    user_id = context["user"]["id"]
    if not user_id:
        context.update({"library": None, "is_owner": True, "visibility_levels": constants.VISIBILITY_LEVELS})
        return render_page("apps/shelf/library/collection.html", context=context)
    return _render_library(context, user_id)


@blueprint.route("/users/<user_id>", methods=["GET"])
def get_user_library_page(user_id: str):
    """View another user's library, filtered by shelf-api to what the viewer may see."""
    context = get_context()
    return _render_library(context, user_id)


def _render_library(context: dict, user_id: str):
    library = None
    try:
        library = _client().get_library(user_id)
    except Exception:
        current_app.logger.exception("Unable to fetch library for user %s!", user_id)
        flash("Unable to load this library right now.")
    context.update(
        {
            "library": library,
            "is_owner": context["user"]["id"] == user_id,
            "visibility_levels": constants.VISIBILITY_LEVELS,
        }
    )
    return render_page("apps/shelf/library/collection.html", context=context)


@blueprint.route("/default-visibility/preview", methods=["POST"])
def preview_default_visibility():
    """Preview which entries would become newly exposed by a default-visibility change."""
    context = get_context()
    user_id = context["user"]["id"]
    visibility = request.form.get("visibility") or request.json.get("visibility")
    try:
        preview = _client().preview_library_default_visibility(user_id, visibility)
        return jsonify(preview)
    except Exception:
        current_app.logger.exception("Unable to preview default visibility change for user %s!", user_id)
        return jsonify({"error": "Unable to preview this change right now."}), 502


@blueprint.route("/default-visibility", methods=["POST"])
def set_default_visibility():
    """Apply a default-visibility change, with optional per-entry overrides from the warning dialog."""
    context = get_context()
    user_id = context["user"]["id"]
    visibility = request.form.get("visibility")
    overrides = request.form.get("overrides")
    try:
        _client().set_library_default_visibility(user_id, visibility, overrides)
        flash("Library default visibility updated.")
    except Exception:
        current_app.logger.exception("Unable to set default visibility for user %s!", user_id)
        flash("Unable to update your library's default visibility right now.")
    return redirect(url_for("web.library.get_library_page"))


@blueprint.route("/entries/<volume_id>/visibility", methods=["POST"])
def set_entry_visibility(volume_id: str):
    """Set (or clear) a per-entry visibility override."""
    context = get_context()
    user_id = context["user"]["id"]
    visibility = request.form.get("visibility") or None
    try:
        _client().set_library_entry_visibility(user_id, volume_id, visibility)
    except Exception:
        current_app.logger.exception(
            "Unable to set visibility override for volume %s (user %s)!", volume_id, user_id
        )
        flash("Unable to update that entry's visibility right now.")
    return redirect(url_for("web.library.get_library_page"))


@blueprint.route("/entries/<volume_id>", methods=["POST"])
def remove_entry(volume_id: str):
    """Remove a volume from the library."""
    context = get_context()
    user_id = context["user"]["id"]
    if request.form.get("_method") == "DELETE":
        try:
            _client().remove_library_entry(user_id, volume_id)
        except Exception:
            current_app.logger.exception("Unable to remove volume %s from library (user %s)!", volume_id, user_id)
            flash("Unable to remove that volume right now.")
    return redirect(url_for("web.library.get_library_page"))
