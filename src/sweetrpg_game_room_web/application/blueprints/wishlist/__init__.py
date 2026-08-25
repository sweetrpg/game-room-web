# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Wishlist routes.
"""

from flask import Blueprint, current_app, request, flash, redirect, url_for
from sweetrpg_game_room_web.application import constants
from sweetrpg_web_core.helpers.context import get_context
from sweetrpg_game_room_web.application.blueprints import render_page


blueprint = Blueprint("wishlist", __name__, url_prefix="/wishlist")


def _client():
    return current_app.config[constants.SHELF_CLIENT_KEY]


@blueprint.route("/", methods=["GET"])
def get_wishlist_page():
    """Get the current user's wishlist page."""
    context = get_context()
    user_id = context["user"]["id"]
    wishlist = None
    if user_id:
        try:
            wishlist = _client().get_wishlist(user_id)
        except Exception:
            current_app.logger.exception("Unable to fetch wishlist for user %s!", user_id)
            flash("Unable to load your wishlist right now.")
    context.update(
        {
            "wishlist": wishlist,
            "visibility_levels": constants.VISIBILITY_LEVELS,
        }
    )
    return render_page("apps/shelf/wishlist/collection.html", context=context)


@blueprint.route("/visibility", methods=["POST"])
def set_visibility():
    """Set the wishlist's own visibility - independent of the library's default."""
    context = get_context()
    user_id = context["user"]["id"]
    visibility = request.form.get("visibility")
    try:
        _client().set_wishlist_visibility(user_id, visibility)
        flash("Wishlist visibility updated.")
    except Exception:
        current_app.logger.exception("Unable to set wishlist visibility for user %s!", user_id)
        flash("Unable to update your wishlist's visibility right now.")
    return redirect(url_for("web.wishlist.get_wishlist_page"))


@blueprint.route("/entries/<volume_id>", methods=["POST"])
def remove_entry(volume_id: str):
    """Remove a volume from the wishlist."""
    context = get_context()
    user_id = context["user"]["id"]
    if request.form.get("_method") == "DELETE":
        try:
            _client().remove_wishlist_entry(user_id, volume_id)
        except Exception:
            current_app.logger.exception("Unable to remove volume %s from wishlist (user %s)!", volume_id, user_id)
            flash("Unable to remove that volume right now.")
    return redirect(url_for("web.wishlist.get_wishlist_page"))
