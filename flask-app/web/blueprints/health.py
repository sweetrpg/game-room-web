# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')
