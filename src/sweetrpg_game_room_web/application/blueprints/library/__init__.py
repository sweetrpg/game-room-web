# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Library routes.
"""

from flask import Blueprint, current_app, request, jsonify, flash
from flask_babel import gettext as _
from sweetrpg_game_room_web.application import constants
from sweetrpg_web_core.helpers.context import get_context
from sweetrpg_game_room_web.application.blueprints import (
    render_page,
    local_redirect,
    _format_date,
    _recent_entries,
)
from sweetrpg_game_room_web.application.constants import (
    RESPONSE_400_VOLUME_REQUIRED,
    RESPONSE_502_UNABLE_TO_ADD_VOLUME,
)


blueprint = Blueprint("library", __name__, url_prefix="/library")


def _client():
    return current_app.config[constants.GAME_ROOM_CLIENT_KEY]


def _catalog_client():
    return current_app.config[constants.CATALOG_CLIENT_KEY]


@blueprint.route("/", methods=["GET"])
def get_library_page():
    """Get the current user's library page."""
    context = get_context()
    user_id = context["user"]["id"]
    if not user_id:
        context.update({"library": None, "is_owner": True, "visibility_levels": constants.VISIBILITY_LEVELS})
        return render_page("apps/game-room/library/collection.html", context=context)
    return _render_library(context, user_id)


@blueprint.route("/users/<user_id>", methods=["GET"])
def get_user_library_page(user_id: str):
    """View another user's library, filtered by game-room-api to what the viewer may see."""
    context = get_context()
    return _render_library(context, user_id)


def _render_library(context: dict, user_id: str):
    library = None
    try:
        library = _client().get_library(user_id)
    except Exception:
        current_app.logger.exception("Unable to fetch library for user %s!", user_id)
        flash(_("Unable to load this library right now."))
    context.update(
        {
            "library": library,
            "is_owner": context["user"]["id"] == user_id,
            "visibility_levels": constants.VISIBILITY_LEVELS,
        }
    )
    return render_page("apps/game-room/library/collection.html", context=context)


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
        return jsonify({"error": _("Unable to preview this change right now.")}), 502


@blueprint.route("/default-visibility", methods=["POST"])
def set_default_visibility():
    """Apply a default-visibility change, with optional per-entry overrides from the warning dialog."""
    context = get_context()
    user_id = context["user"]["id"]
    visibility = request.form.get("visibility")
    overrides = request.form.get("overrides")
    try:
        _client().set_library_default_visibility(user_id, visibility, overrides)
        flash(_("Library default visibility updated."))
    except Exception:
        current_app.logger.exception("Unable to set default visibility for user %s!", user_id)
        flash(_("Unable to update your library's default visibility right now."))
    return local_redirect("web.library.get_library_page")


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
        flash(_("Unable to update that entry's visibility right now."))
    return local_redirect("web.library.get_library_page")


@blueprint.route("/entries/visibility/bulk", methods=["POST"])
def set_bulk_entry_visibility():
    """Apply a visibility override to multiple selected library entries at once."""
    context = get_context()
    user_id = context["user"]["id"]
    visibility = request.form.get("visibility") or None
    raw = request.form.get("volume_ids") or ""
    volume_ids = [v for v in (s.strip() for s in raw.split(",")) if v]
    if not volume_ids:
        flash(_("Select at least one entry first."))
        return local_redirect("web.library.get_library_page")
    failed = []
    for volume_id in volume_ids:
        try:
            _client().set_library_entry_visibility(user_id, volume_id, visibility)
        except Exception:
            current_app.logger.exception(
                "Unable to set visibility override for volume %s (user %s)!", volume_id, user_id
            )
            failed.append(volume_id)
    if failed:
        flash(_("Unable to update visibility for some entries right now."))
        return local_redirect("web.library.get_library_page", failed=",".join(failed))
    flash(_("Entry visibility updated."))
    return local_redirect("web.library.get_library_page")


@blueprint.route("/volume-search", methods=["GET"])
def search_volumes():
    """Search catalog-api for volumes by title, for the add-to-library dialog."""
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])
    try:
        return jsonify(_catalog_client().search_volumes(query))
    except Exception:
        current_app.logger.exception("Unable to search volumes for query %r!", query)
        return jsonify([]), 502


@blueprint.route("/entries", methods=["POST"])
def add_entry():
    """Add a volume to the current user's library, for the landing page's add-to-library dialog.

    Returns the library's updated count/recent list as JSON so the caller can refresh the
    landing page's Library card in place, without a full page reload.
    """
    context = get_context()
    current_app.logger.info("Adding volume to library", extra={"context": context})

    user_id = context["user"]["id"]
    payload = request.json or {}
    volume_id = (payload.get("volume_id") or "").strip()
    if not volume_id:
        return jsonify({"code": RESPONSE_400_VOLUME_REQUIRED, "error": _("A volume is required.")}), 400
    try:
        _client().add_library_entry(user_id, volume_id, volume_title=(payload.get("volume_title") or "").strip())
        library = _client().get_library(user_id) or {}
        entries = library.get("entries") or []
        return jsonify(
            {
                "count": len(entries),
                "recent": [
                    {**e, "added_at_label": _format_date(e.get("added_at"))}
                    for e in _recent_entries(entries, "added_at")
                ],
            }
        )
    except Exception:
        current_app.logger.exception("Unable to add volume %s to library (user %s)!", volume_id, user_id)
        return jsonify({"code": RESPONSE_502_UNABLE_TO_ADD_VOLUME, "error": _("Unable to add that volume right now.")}), 502


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
            flash(_("Unable to remove that volume right now."))
    return local_redirect("web.library.get_library_page")
