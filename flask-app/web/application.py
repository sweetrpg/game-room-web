"""
application.py
- creates a Flask app instance and registers the database object
"""


from flask import Flask, jsonify, render_template
from flask_cors import CORS
# from flask_vue import Vue


def create_app(app_name='SURVEY_API'):
    # configuration
    DEBUG = True

    # instantiate the app
    app = Flask(__name__)
    app.config.from_object(__name__)

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})


    app = Flask(app_name)
    app.config.from_object('web.config.BaseConfig')

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # # setup Vue
    # app.config['VUE_USE_MINIFIED'] = True
    # app.config['VUE_CDN_FORCE_SSL'] = True
    # app.config['VUE_SERVE_LOCAL'] = False
    # app.config['VUE_LOCAL_SUBDOMAIN'] = 'sweetrpg.com'
    # app.config['VUE_CONFIGURATION'] = {}
    # Vue(app)

    from web.blueprints import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from web.db import db
    db.init_app(app)

    return app
