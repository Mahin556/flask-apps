from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data store
items = {}
next_id = 1

# Create
@app.route('/items', methods=['POST'])
def create_item():
    global next_id
    data = request.get_json()
    item = {
        "id": next_id,
        "name": data.get("name", ""),
        "value": data.get("value", "")
    }
    items[next_id] = item
    next_id += 1
    return jsonify(item), 201

# Read all
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(list(items.values()))

# Read one
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = items.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)

# Update
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = items.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    data = request.get_json()
    item["name"] = data.get("name", item["name"])
    item["value"] = data.get("value", item["value"])
    return jsonify(item)

# Delete
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id not in items:
        return jsonify({"error": "Item not found"}), 404
    deleted = items.pop(item_id)
    return jsonify(deleted)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
