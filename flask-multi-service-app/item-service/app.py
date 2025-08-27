import os
import time
import requests
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from sqlalchemy.exc import OperationalError

app = Flask(__name__)

# ---------------- CONFIG ----------------
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "item_service")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:5000")  # User service must be running

# ---------------- MODELS ----------------
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100))

    def to_dict(self):
        return {"id": self.id, "name": self.name, "value": self.value}

max_retries = 10    ### LOGIC ---> Wait for DB service to UP
for i in range(max_retries):
    try:
        with app.app_context():
            db.create_all()
        print("✅ Database connected and tables created")
        break
    except OperationalError:
        print(f"⏳ Database not ready, retrying {i+1}/{max_retries}...")
        time.sleep(5)
else:
    raise Exception("❌ Database not available after retries")

# ---------------- HELPER ----------------
def validate_api_key(api_key):
    response = requests.post(f"{USER_SERVICE_URL}/validate", json={"api_key": api_key})
    return response.status_code == 200 and response.json().get("valid")

# ---------------- ROUTES ----------------
@app.route("/items", methods=["POST"])
def create_item():
    api_key = request.headers.get("X-API-KEY")
    if not validate_api_key(api_key):
        return jsonify({"error": "Invalid API key"}), 403

    data = request.get_json()
    item = Item(name=data.get("name"), value=data.get("value"))
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@app.route("/items", methods=["GET"])
def get_items():
    api_key = request.headers.get("X-API-KEY")
    if not validate_api_key(api_key):
        return jsonify({"error": "Invalid API key"}), 403

    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])


@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    api_key = request.headers.get("X-API-KEY")
    if not validate_api_key(api_key):
        return jsonify({"error": "Invalid API key"}), 403

    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item.to_dict())


@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    api_key = request.headers.get("X-API-KEY")
    if not validate_api_key(api_key):
        return jsonify({"error": "Invalid API key"}), 403

    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()
    item.name = data.get("name", item.name)
    item.value = data.get("value", item.value)
    db.session.commit()
    return jsonify(item.to_dict())


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    api_key = request.headers.get("X-API-KEY")
    if not validate_api_key(api_key):
        return jsonify({"error": "Invalid API key"}), 403

    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify(item.to_dict())


if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")
