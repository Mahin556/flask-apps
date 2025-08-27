import os
import time
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from sqlalchemy.exc import OperationalError

app = Flask(__name__)


# ---------------- CONFIG ----------------
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "user_service")


app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------- MODELS ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    api_key = db.Column(db.String(100), unique=True, nullable=False)

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

# ---------------- ROUTES ----------------
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


@app.route("/validate", methods=["POST"])
def validate():
    """Validate API key from Item Service"""
    data = request.get_json()
    api_key = data.get("api_key")

    user = User.query.filter_by(api_key=api_key).first()
    if user:
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False}), 403


if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")
