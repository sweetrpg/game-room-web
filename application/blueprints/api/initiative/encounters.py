__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
encounters.py
- Encounters API
"""


from application.blueprints.api import blueprint


@blueprint.route('/encounters')
def get_encounters():
    return {
        'encounters': [
        {
            'id': "1",
            'name': "TODO",
            'gameSystem': "dnd5e",
            'participantCount': 3,
            'isFavorite': False
        }
    ]
    }
