__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
stripe.py
- Stripe-specific endpoints
"""


from flask import jsonify, request, current_app
from application.blueprints.billing import blueprint
import stripe


@blueprint.route('/stripe/webhook')
def stripe_webhook():
    """
    Endpoint for Stripe webhook calls.
    """

    # verify signature
    payload = request.data
    try:
        sig_header = request.headers['Stripe-Signature']
        event = stripe.Webhook.construct_event(payload,
                sig_header,
                current_app.config.STRIPE_SIGNING_SECRET)
    except ValueError as e:
        # Invalid payload
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify({'error': 'Invalid signature'}), 400


    # TODO

    return jsonify({}), 204
