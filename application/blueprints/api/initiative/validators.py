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
        'game_system': {
            'type': 'string'
        },
        'ordering': {
            'type': 'string',
            'pattern': '^(high-to-low|low-to-high|pc-v-adversary|player-managed)$'
        },
        'tie_breaker': {
            'type': 'string',
            'pattern': '^(query|random|alpha)$'
        },
        'theme': {
            'type': 'string'
        },
        'flags': {
            'type': 'array',
            'items': { 'type': 'string' }
        },
    },
    'required': ['name', 'game_system']
}

class CreateEncounterInput(Inputs):
    json = [JsonSchema(schema=create_encounter_schema)]


create_group_schema = {
    '$id': 'http://sweetrpg.com/schemas/create_group.json',
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
        },
        'flags': {
            'type': 'array',
            'items': { 'type': 'string' }
        },
    },
    'required': ['name']
}

class CreateGroupInput(Inputs):
    json = [JsonSchema(schema=create_group_schema)]


add_encounter_participant_schema = {
    '$id': 'http://sweetrpg.com/schemas/add_encounter_participant.json',
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
        },
        'flags': {
            'type': 'array',
            'items': { 'type': 'string' }
        },
    },
    'required': ['name', 'type']
}


class AddEncounterParticipantInput(Inputs):
    json = [JsonSchema(schema=add_encounter_participant_schema)]


update_encounter_schema = {
    '$id': 'http://sweetrpg.com/schemas/update_encounter.json',
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
        },
        'flags': {
            'type': 'array',
            'items': { 'type': 'string' }
        },
    },
    'required': []
}

class UpdateEncounterInput(Inputs):
    json = [JsonSchema(schema=update_encounter_schema)]


update_encounter_participant_schema = {
    '$id': 'http://sweetrpg.com/schemas/update_encounter_participant.json',
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

class UpdateEncounterParticipantInput(Inputs):
    json = [JsonSchema(schema=update_encounter_participant_schema)]


update_session_schema = {
    '$id': 'http://sweetrpg.com/schemas/update_session.json',
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'current_participant_index': {
            'type': 'number'
        },
        'flags': {
            'type': 'array',
            'items': { 'type': 'string' }
        },
    },
    'required': []
}


class UpdateSessionInput(Inputs):
    json = [JsonSchema(schema=update_session_schema)]


update_participant_order_schema = {
    '$id': 'http://sweetrpg.com/schemas/update_session.json',
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
    },
    'required': []
}


class UpdateParticipantOrderInput(Inputs):
    json = [JsonSchema(schema=update_participant_order_schema)]


add_group_participant_schema = {
    '$id': 'http://sweetrpg.com/schemas/add_group_participant.json',
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
        },
        'flags': {
            'type': 'array',
            'items': { 'type': 'string' }
        },
    },
    'required': ['name', 'type']
}

class AddGroupParticipantInput(Inputs):
    json = [JsonSchema(schema=add_group_participant_schema)]


update_group_participant_schema = {
    '$id': 'http://sweetrpg.com/schemas/update_group_participant.json',
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
        'notes': {
            'type': 'string'
        },
        'image': {
            'type': 'string'
        },
        'external_key': {
            'type': 'string'
        }
    },
    'required': []
}

class UpdateGroupParticipantInput(Inputs):
    json = [JsonSchema(schema=update_group_participant_schema)]
