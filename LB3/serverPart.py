from flask import Flask, jsonify, request, make_response
from functools import wraps

app = Flask(__name__)

catalog = [
    {
        'id': 1,
        'name': 'T-Shirt',
        'price': 25.00,
        'size': 'M',
        'color': 'Blue'
    },
    {
        'id': 2,
        'name': 'Jeans',
        'price': 50.50,
        'size': 'L',
        'color': 'Black'
    }
]

users = {
    "kolden": "koldenPass",
    "kolden1": "koldenPass1"
}


def check_auth(username, password):
    return username in users and users[username] == password


def authenticate():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401,
                         {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@app.route('/items', methods=['GET'])
@requires_auth
def get_items():
    return jsonify(catalog)


@app.route('/items/<int:item_id>', methods=['GET'])
@requires_auth
def get_item(item_id):
    item = next((item for item in catalog if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({'error': 'Item not found'}), 404


@app.route('/items', methods=['POST'])
@requires_auth
def create_item():
    if not request.json or not 'name' in request.json:
        return jsonify({'error': 'Bad request, name is required'}), 400

    new_id = catalog[-1]['id'] + 1 if catalog else 1

    new_item = {
        'id': new_id,
        'name': request.json['name'],
        'price': request.json.get('price', 0.0),
        'size': request.json.get('size', 'Unknown'),
        'color': request.json.get('color', 'Unknown')
    }
    catalog.append(new_item)
    return jsonify(new_item), 201


@app.route('/items/<int:item_id>', methods=['PUT'])
@requires_auth
def update_item(item_id):
    item = next((item for item in catalog if item['id'] == item_id), None)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    if not request.json:
        return jsonify({'error': 'Bad request'}), 400

    item['name'] = request.json.get('name', item['name'])
    item['price'] = request.json.get('price', item['price'])
    item['size'] = request.json.get('size', item['size'])
    item['color'] = request.json.get('color', item['color'])

    return jsonify(item)


@app.route('/items/<int:item_id>', methods=['DELETE'])
@requires_auth
def delete_item(item_id):
    item = next((item for item in catalog if item['id'] == item_id), None)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    catalog.remove(item)
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True, port=8000)