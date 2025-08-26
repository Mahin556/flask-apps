from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Load environment variables
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "flask_crud")

# MySQL database configuration
# Format: mysql+pymysql://username:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "value": self.value}


# Initialize database tables
with app.app_context():
    db.create_all()

# ------------------- CRUD ROUTES -------------------

# Create
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    item = Item(name=data.get("name", ""), value=data.get("value", ""))
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

# Read all
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

# Read one
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item.to_dict())

# Update
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    data = request.get_json()
    item.name = data.get("name", item.name)
    item.value = data.get("value", item.value)
    db.session.commit()
    return jsonify(item.to_dict())

# Delete
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify(item.to_dict())

# ------------------- RUN APP -------------------
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
