__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""


from application.blueprints.apps import blueprint
from application.blueprints import requires_auth, render_page
from application.models.initiative.encounter import Encounter
from application.blueprints import error_page


@blueprint.route('/initiative/encounters/<int:encounter_id>')
@requires_auth
def encounter_main(encounter_id: int):
    encounter = Encounter.query.filter_by(id=encounter_id).first()
    if not encounter:
        return error_page("That encounter could not be found.", 404)

    context = {
        'name': encounter.name,
        'id': encounter.id,
    }
    return render_page('apps/initiative/encounter.html', context=context)
