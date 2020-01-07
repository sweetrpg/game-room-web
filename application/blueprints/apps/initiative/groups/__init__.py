__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
- Groups
"""


from application.blueprints.apps import blueprint
from application.blueprints import requires_auth, render_page
from application.models.initiative.participant import ParticipantGroup
from application.blueprints import error_page


@blueprint.route('/initiative/groups/<int:group_id>')
@requires_auth
def groups_main(group_id: int):
    group = ParticipantGroup.query.filter_by(id=group_id).first()
    if not group:
        return error_page("That group could not be found.", 404)

    context = {
        'name': group.name,
        'id': group.id,
    }
    return render_page('apps/initiative/group.html', context=context)
