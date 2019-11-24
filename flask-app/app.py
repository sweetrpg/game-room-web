from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_vue import Vue


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# setup Vue
app.config['VUE_USE_MINIFIED'] = True
app.config['VUE_CDN_FORCE_SSL'] = True
app.config['VUE_SERVE_LOCAL'] = False
app.config['VUE_LOCAL_SUBDOMAIN'] = 'sweetrpg.com'
app.config['VUE_CONFIGURATION'] = {}
Vue(app)

# main page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    app.run()
