__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
validators.py
- Validators for API calls
"""


from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema


create_encounter_schema = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
        },
        'gameSystem': {
            'type': 'string'
        },
        'ordering': {
            'type': 'string',
            'pattern': '^(high-to-low|low-to-high|pc-v-adversary|player-managed)$'
        },
        'theme': {
            'type': 'string'
        }
    },
    'required': ['name', 'gameSystem']
}


class CreateEncounterInput(Inputs):
    json = [JsonSchema(schema=create_encounter_schema)]
