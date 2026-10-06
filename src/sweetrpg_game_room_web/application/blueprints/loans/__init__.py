# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Loans routes.
"""

from flask import Blueprint, current_app, request, jsonify, flash
from flask_babel import gettext as _
from sweetrpg_game_room_web.application import constants
from sweetrpg_web_core.helpers.context import get_context
from sweetrpg_game_room_web.application.blueprints import (
    render_page,
    local_redirect,
)


blueprint = Blueprint("loans", __name__, url_prefix="/loans")


def _client():
    return current_app.config[constants.GAME_ROOM_CLIENT_KEY]


def _catalog_client():
    return current_app.config[constants.CATALOG_CLIENT_KEY]


@blueprint.route("/", methods=["GET"])
def get_loans_page():
    """List the current user's loans: what they lent out and what they borrowed."""
    context = get_context()
    user_id = context["user"]["id"]
    if not user_id:
        context.update({"loans_out": [], "loans_borrowed": []})
        return render_page("apps/game-room/loans/collection.html", context=context)

    loans_out, loans_borrowed = [], []
    try:
        loans_out = _client().list_loans_lent(user_id) or []
    except Exception:
        current_app.logger.exception("Unable to list loaned-out volumes for user %s!", user_id)
        flash(_("Unable to load your loans right now."))
    try:
        loans_borrowed = _client().list_loans_borrowed(user_id) or []
    except Exception:
        current_app.logger.exception("Unable to list borrowed volumes for user %s!", user_id)
        flash(_("Unable to load your borrowed volumes right now."))

    context.update({"loans_out": loans_out, "loans_borrowed": loans_borrowed})
    return render_page("apps/game-room/loans/collection.html", context=context)


@blueprint.route("/new", methods=["GET"])
def new_loan_page():
    """Show the create-loan form: pick a volume and a borrower (platform user or free-form name).

    volume_id/volume_title may arrive pre-filled via query string - used by the library page's
    per-entry "Lend" action, which already knows which volume the lender picked.
    """
    context = get_context()
    context.update(
        {
            "prefill_volume_id": request.args.get("volume_id", ""),
            "prefill_volume_title": request.args.get("volume_title", ""),
        }
    )
    return render_page("apps/game-room/loans/form.html", context=context)


@blueprint.route("/", methods=["POST"])
def create_loan():
    """Lend a volume to a platform user (by id) or a free-form name (exactly one required).

    A platform-linked borrower also requires a display name alongside the id - the API stores it
    as a snapshot of that user's current display name, so the caller must supply it (it does not
    resolve the name server-side).
    """
    context = get_context()
    user_id = context["user"]["id"]
    volume_id = request.form.get("volume_id", "").strip()
    borrower_user_id = request.form.get("borrower_user_id", "").strip()
    borrower_name = request.form.get("borrower_name", "").strip()

    if not volume_id:
        flash(_("A volume is required."))
        return local_redirect("web.loans.new_loan_page")
    if not borrower_user_id and not borrower_name:
        flash(_("A borrower - either a platform user or a name - is required."))
        return local_redirect("web.loans.new_loan_page")
    if borrower_user_id and not borrower_name:
        flash(_("A display name is required for a platform user."))
        return local_redirect("web.loans.new_loan_page")

    try:
        _client().create_loan(
            user_id, volume_id, borrower_user_id=borrower_user_id or None, borrower_name=borrower_name or None
        )
        flash(_("Loan recorded."))
    except Exception:
        current_app.logger.exception("Unable to create loan for volume %s (user %s)!", volume_id, user_id)
        flash(_("Unable to record that loan right now."))
        return local_redirect("web.loans.new_loan_page")
    return local_redirect("web.loans.get_loans_page")


@blueprint.route("/bulk", methods=["POST"])
def create_bulk_loan():
    """Lend every selected library volume to one borrower at once, from the library page's
    multi-select bulk action.

    Same borrower rules as the single-create form (name always required, alongside a platform
    user ID when one is given). One loan is created per selected volume; a volume that fails
    doesn't block the rest - mirrors the library bulk-visibility action's partial-failure
    handling.
    """
    context = get_context()
    user_id = context["user"]["id"]
    raw = request.form.get("volume_ids") or ""
    volume_ids = [v for v in (s.strip() for s in raw.split(",")) if v]
    borrower_user_id = request.form.get("borrower_user_id", "").strip()
    borrower_name = request.form.get("borrower_name", "").strip()

    if not volume_ids:
        flash(_("Select at least one volume first."))
        return local_redirect("web.library.get_library_page")
    if not borrower_user_id and not borrower_name:
        flash(_("A borrower - either a platform user or a name - is required."))
        return local_redirect("web.library.get_library_page")
    if borrower_user_id and not borrower_name:
        flash(_("A display name is required for a platform user."))
        return local_redirect("web.library.get_library_page")

    failed = []
    for volume_id in volume_ids:
        try:
            _client().create_loan(
                user_id, volume_id, borrower_user_id=borrower_user_id or None, borrower_name=borrower_name or None
            )
        except Exception:
            current_app.logger.exception("Unable to create loan for volume %s (user %s)!", volume_id, user_id)
            failed.append(volume_id)
    if failed:
        flash(_("Unable to lend some volumes right now."))
        return local_redirect("web.library.get_library_page", failed=",".join(failed))
    flash(_("Volumes lent."))
    return local_redirect("web.library.get_library_page")


@blueprint.route("/<loan_id>/return", methods=["POST"])
def return_loan(loan_id: str):
    """Mark a loan the current user lent out as returned."""
    context = get_context()
    user_id = context["user"]["id"]
    try:
        _client().return_loan(user_id, loan_id)
        flash(_("Loan marked as returned."))
    except Exception:
        current_app.logger.exception("Unable to mark loan %s returned (user %s)!", loan_id, user_id)
        flash(_("Unable to mark that loan as returned right now."))
    return local_redirect("web.loans.get_loans_page")


@blueprint.route("/<loan_id>", methods=["POST"])
def delete_loan(loan_id: str):
    """Delete a loan (method-override form, mirrors the wishlist/table delete pattern)."""
    context = get_context()
    user_id = context["user"]["id"]
    if request.form.get("_method") == "DELETE":
        try:
            _client().delete_loan(user_id, loan_id)
            flash(_("Loan deleted."))
        except Exception:
            current_app.logger.exception("Unable to delete loan %s (user %s)!", loan_id, user_id)
            flash(_("Unable to delete that loan right now."))
    return local_redirect("web.loans.get_loans_page")


@blueprint.route("/volume-search", methods=["GET"])
def search_volumes():
    """Search catalog-api for volumes by title, for the create-loan form."""
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])
    try:
        return jsonify(_catalog_client().search_volumes(query))
    except Exception:
        current_app.logger.exception("Unable to search volumes for query %r!", query)
        return jsonify([]), 502
