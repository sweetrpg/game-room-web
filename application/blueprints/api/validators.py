__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
validators.py
- Validators for API calls
"""


from flask import current_app
from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from functools import wraps
from werkzeug.exceptions import BadRequest


def validate_payload(validator, request: object):
    current_app.logger.info(f"Validating request {request} using {validator}")
    inputs = validator(request)
    current_app.logger.debug(f"inputs: {inputs}")
    if not inputs.validate():
        current_app.logger.debug(f"errors: {inputs.errors}")
        raise BadRequest(inputs.errors)

    current_app.logger.info("Payload is valid.")
