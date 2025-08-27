import secrets
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///apikey.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ------------------- MODELS -------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    api_key = db.Column(db.String(100), unique=True, nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100))

    def to_dict(self):
        return {"id": self.id, "name": self.name, "value": self.value}

with app.app_context():
    db.create_all()

# ------------------- HELPER -------------------
def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY")
        if not api_key:
            return jsonify({"error": "API key required"}), 401
        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            return jsonify({"error": "Invalid API key"}), 403
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# ------------------- AUTH ROUTES -------------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    api_key = secrets.token_hex(16)
    user = User(username=username, api_key=api_key)
    db.session.add(user)
    db.session.commit()

    return jsonify({"username": username, "api_key": api_key}), 201

# ------------------- PROTECTED CRUD ROUTES -------------------
@app.route("/items", methods=["POST"])
@require_api_key
def create_item():
    data = request.get_json()
    item = Item(name=data.get("name"), value=data.get("value"))
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@app.route("/items", methods=["GET"])
@require_api_key
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

@app.route("/items/<int:item_id>", methods=["GET"])
@require_api_key
def get_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item.to_dict())

@app.route("/items/<int:item_id>", methods=["PUT"])
@require_api_key
def update_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    data = request.get_json()
    item.name = data.get("name", item.name)
    item.value = data.get("value", item.value)
    db.session.commit()
    return jsonify(item.to_dict())

@app.route("/items/<int:item_id>", methods=["DELETE"])
@require_api_key
def delete_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify(item.to_dict())

# ------------------- RUN APP -------------------
if __name__ == "__main__":
    app.run(debug=True)
