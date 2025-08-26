from flask import Flask, request, jsonify
import redis
import json
import uuid
import os

app = Flask(__name__)

# Load from environment variables with defaults
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB   = int(os.getenv("REDIS_DB", 0))

# Create Redis connection
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True
)

# ------------------- CRUD ROUTES -------------------

# Create
@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    item_id = str(uuid.uuid4())  # unique ID
    item = {"id": item_id, "name": data.get("name", ""), "value": data.get("value", "")}
    r.set(item_id, json.dumps(item))
    return jsonify(item), 201

# Read all
@app.route("/items", methods=["GET"])
def get_items():
    keys = r.keys()
    items = [json.loads(r.get(k)) for k in keys]
    return jsonify(items)

# Read one
@app.route("/items/<string:item_id>", methods=["GET"])
def get_item(item_id):
    item = r.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(json.loads(item))

# Update
@app.route("/items/<string:item_id>", methods=["PUT"])
def update_item(item_id):
    item = r.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    data = request.get_json()
    item = json.loads(item)
    item["name"] = data.get("name", item["name"])
    item["value"] = data.get("value", item["value"])
    r.set(item_id, json.dumps(item))
    return jsonify(item)

# Delete
@app.route("/items/<string:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = r.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    r.delete(item_id)
    return jsonify(json.loads(item))

# ------------------- RUN APP -------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
