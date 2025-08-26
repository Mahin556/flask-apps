from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from pymongo import ReturnDocument
import os

app = Flask(__name__)

# Load environment variables
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "flask_crud")

# MongoDB configuration
app.config["MONGO_URI"] = f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:27017/{DB_NAME}?authSource=admin"
mongo = PyMongo(app)

# Helper: convert MongoDB document to dict with string id
def item_to_dict(item):
    return {
        "id": str(item["_id"]),
        "name": item.get("name", ""),
        "value": item.get("value", "")
    }

# ------------------- CRUD ROUTES -------------------

# Create
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = {
        "name": data.get("name", ""),
        "value": data.get("value", "")
    }
    result = mongo.db.items.insert_one(new_item)
    new_item["_id"] = result.inserted_id
    return jsonify(item_to_dict(new_item)), 201

# Read all
@app.route('/items', methods=['GET'])
def get_items():
    items = mongo.db.items.find()
    return jsonify([item_to_dict(item) for item in items])

# Read one
@app.route('/items/<string:item_id>', methods=['GET'])
def get_item(item_id):
    try:
        item = mongo.db.items.find_one({"_id": ObjectId(item_id)})
    except:
        return jsonify({"error": "Invalid ObjectId"}), 400
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item_to_dict(item))

# Update
@app.route('/items/<string:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    try:
        updated = mongo.db.items.find_one_and_update(
            {"_id": ObjectId(item_id)},
            {"$set": {"name": data.get("name"), "value": data.get("value")}},
            return_document=ReturnDocument.AFTER  # ✅ correct usage
        )
    except:
        return jsonify({"error": "Invalid ObjectId"}), 400

    if not updated:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item_to_dict(updated))

# Delete
@app.route('/items/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        deleted = mongo.db.items.find_one_and_delete({"_id": ObjectId(item_id)})
    except:
        return jsonify({"error": "Invalid ObjectId"}), 400

    if not deleted:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item_to_dict(deleted))

# ------------------- RUN APP -------------------
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)