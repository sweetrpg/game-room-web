# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Wishlist routes.
"""

from flask import Blueprint, current_app, request, flash
from flask_babel import gettext as _
from sweetrpg_game_room_web.application import constants
from sweetrpg_web_core.helpers.context import get_context
from sweetrpg_game_room_web.application.blueprints import (
    render_page,
    local_redirect,
)


blueprint = Blueprint("wishlist", __name__, url_prefix="/wishlist")


def _client():
    return current_app.config[constants.GAME_ROOM_CLIENT_KEY]


@blueprint.route("/", methods=["GET"])
def get_wishlists_page():
    """List the current user's wishlists."""
    context = get_context()
    user_id = context["user"]["id"]
    if not user_id:
        context.update({"wishlists": [], "is_owner": True})
        return render_page("apps/game-room/wishlist/collection.html", context=context)
    return _render_wishlists_list(context, user_id)


@blueprint.route("/users/<user_id>", methods=["GET"])
def get_user_wishlists_page(user_id: str):
    """View another user's wishlists, filtered by game-room-api to what the viewer may see."""
    context = get_context()
    return _render_wishlists_list(context, user_id)


def _render_wishlists_list(context: dict, user_id: str):
    wishlists = []
    try:
        wishlists = _client().list_wishlists(user_id) or []
    except Exception:
        current_app.logger.exception("Unable to list wishlists for user %s!", user_id)
        flash(_("Unable to load these wishlists right now."))
    context.update(
        {
            "wishlists": wishlists,
            "is_owner": context["user"]["id"] == user_id,
            "wishlists_owner_id": user_id,
        }
    )
    return render_page("apps/game-room/wishlist/collection.html", context=context)


@blueprint.route("/new", methods=["GET"])
def new_wishlist_page():
    """Show the create-wishlist form. Visibility defaults to private."""
    context = get_context()
    context.update({"visibility_levels": constants.VISIBILITY_LEVELS, "default_visibility": "private"})
    return render_page("apps/game-room/wishlist/form.html", context=context)


@blueprint.route("/", methods=["POST"])
def create_wishlist():
    """Create a wishlist. Visibility defaults to private if not supplied."""
    context = get_context()
    user_id = context["user"]["id"]
    name = request.form.get("name", "").strip()
    visibility = request.form.get("visibility") or "private"
    if not name:
        flash(_("A wishlist name is required."))
        return local_redirect("web.wishlist.new_wishlist_page")
    try:
        wishlist = _client().create_wishlist(user_id, name, visibility)
        return local_redirect("web.wishlist.get_wishlist_page", wishlist_id=wishlist["id"])
    except Exception:
        current_app.logger.exception("Unable to create wishlist %r for user %s!", name, user_id)
        flash(_("Unable to create that wishlist right now."))
        return local_redirect("web.wishlist.new_wishlist_page")


@blueprint.route("/<wishlist_id>", methods=["GET"])
def get_wishlist_page(wishlist_id: str):
    """Show a wishlist's detail: its entries and visibility (current user's own wishlist)."""
    context = get_context()
    return _render_wishlist(context, context["user"]["id"], wishlist_id)


@blueprint.route("/users/<user_id>/<wishlist_id>", methods=["GET"])
def get_user_wishlist_page(user_id: str, wishlist_id: str):
    """View another user's wishlist, filtered by game-room-api to what the viewer may see."""
    context = get_context()
    return _render_wishlist(context, user_id, wishlist_id)


def _render_wishlist(context: dict, owner_id: str, wishlist_id: str):
    wishlist = None
    try:
        wishlist = _client().get_wishlist(owner_id, wishlist_id)
    except Exception:
        current_app.logger.exception("Unable to fetch wishlist %s for user %s!", wishlist_id, owner_id)
        flash(_("Unable to load this wishlist right now."))
    context.update(
        {
            "wishlist": wishlist,
            "is_owner": context["user"]["id"] == owner_id,
            "visibility_levels": constants.VISIBILITY_LEVELS,
        }
    )
    return render_page("apps/game-room/wishlist/detail.html", context=context)


@blueprint.route("/<wishlist_id>", methods=["POST"])
def update_wishlist(wishlist_id: str):
    """Update a wishlist's visibility, or delete it."""
    context = get_context()
    user_id = context["user"]["id"]
    if request.form.get("_method") == "DELETE":
        try:
            _client().delete_wishlist(user_id, wishlist_id)
            flash(_("Wishlist deleted."))
        except Exception:
            current_app.logger.exception("Unable to delete wishlist %s for user %s!", wishlist_id, user_id)
            flash(_("Unable to delete that wishlist right now."))
        return local_redirect("web.wishlist.get_wishlists_page")

    visibility = request.form.get("visibility") or "private"
    try:
        _client().set_wishlist_visibility(user_id, wishlist_id, visibility)
        flash(_("Wishlist visibility updated."))
    except Exception:
        current_app.logger.exception(
            "Unable to set visibility on wishlist %s for user %s!", wishlist_id, user_id
        )
        flash(_("Unable to update this wishlist's visibility right now."))
    return local_redirect("web.wishlist.get_wishlist_page", wishlist_id=wishlist_id)


@blueprint.route("/<wishlist_id>/entries", methods=["POST"])
def add_wishlist_entry(wishlist_id: str):
    """Add a volume to a wishlist."""
    context = get_context()
    user_id = context["user"]["id"]
    volume_id = request.form.get("volume_id", "").strip()
    volume_title = request.form.get("volume_title", "").strip()
    if volume_id:
        try:
            _client().add_wishlist_entry(user_id, wishlist_id, volume_id, volume_title)
        except Exception:
            current_app.logger.exception(
                "Unable to add volume %s to wishlist %s!", volume_id, wishlist_id
            )
            flash(_("Unable to add that volume right now."))
    return local_redirect("web.wishlist.get_wishlist_page", wishlist_id=wishlist_id)


@blueprint.route("/<wishlist_id>/entries/<volume_id>", methods=["POST"])
def remove_entry(wishlist_id: str, volume_id: str):
    """Remove a volume from a wishlist."""
    context = get_context()
    user_id = context["user"]["id"]
    if request.form.get("_method") == "DELETE":
        try:
            _client().remove_wishlist_entry(user_id, wishlist_id, volume_id)
        except Exception:
            current_app.logger.exception(
                "Unable to remove volume %s from wishlist %s!", volume_id, wishlist_id
            )
            flash(_("Unable to remove that volume right now."))
    return local_redirect("web.wishlist.get_wishlist_page", wishlist_id=wishlist_id)