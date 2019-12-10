__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
validators.py
- Validators for API calls
"""


from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema


create_encounter_schema = {
    '$id': 'http://sweetrpg.com/schemas/create_encounter.json',
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
        'tieBreaker': {
            'type': 'string',
            'pattern': '^(query|random|alpha)$'
        },
        'theme': {
            'type': 'string'
        }
    },
    'required': ['name', 'gameSystem']
}

class CreateEncounterInput(Inputs):
    json = [JsonSchema(schema=create_encounter_schema)]


add_participant_schema = {
    '$id': 'http://sweetrpg.com/schemas/add_participant.json',
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
        },
        'type': {
            'type': 'string',
            'pattern': '^(pc|adversary|object)$'
        },
        'quantity': {
            'type': 'number',
        }
    },
    'required': ['name', 'type']
}


class AddParticipantInput(Inputs):
    json = [JsonSchema(schema=add_participant_schema)]


update_encounter_schema = {
    '$id': 'http://sweetrpg.com/schemas/add_participant.json',
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
        },
        'type': {
            'type': 'string',
            'pattern': '^(pc|adversary|object)$'
        },
        'quantity': {
            'type': 'number',
        }
    },
    'required': ['name', 'type']
}

class UpdateEncounterInput(Inputs):
    json = [JsonSchema(schema=update_encounter_schema)]


update_participant_schema = {
    '$id': 'http://sweetrpg.com/schemas/add_participant.json',
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
        },
        'type': {
            'type': 'string',
            'pattern': '^(pc|adversary|object)$'
        },
        'order': {
            'type': 'number'
        },
        'position': {
            'type': 'number'
        },
        'color': {
            'type': 'string',
            'pattern': r'^\#\d{6}$'
        },
        'marker': {
            'type': 'string'
        },
        'size': {
            'type': 'number'
        },
        'flags': {
            'type': 'array',
            'items': { 'type': 'string' }
        },
        'tag': {
            'type': 'string'
        },
        'notes': {
            'type': 'string'
        },
        'x': {
            'type': 'number'
        },
        'y': {
            'type': 'number'
        },
        'z': {
            'type': 'number'
        },
        'layer': {
            'type': 'string',
            'pattern': '^(normal|background|secret|always)$'
        },
        'hidden': {
            'type': 'boolean'
        },
        'scale': {
            'type': 'number'
        },
    },
    'required': []
}

class UpdateParticipantInput(Inputs):
    json = [JsonSchema(schema=update_participant_schema)]
