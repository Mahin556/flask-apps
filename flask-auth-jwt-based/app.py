from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import mysql.connector
import time
from mysql.connector import Error
import os
import datetime

app = Flask(__name__)

# Load environment variables
DB_USER = os.getenv("DB_USER", "mahin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mahin")
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_NAME = os.getenv("DB_NAME", "flask_crud")

app.config["JWT_SECRET_KEY"] = "supersecretkey"  # change this in production

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# ------------------- DATABASE HELPER -------------------
def get_db_connection(retries=10, delay=5):
    """Try connecting to MySQL with retries."""
    for i in range(retries):
        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST", "mysql"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", "password"),
                database=os.getenv("DB_NAME", "flask_crud"),
            )
            print("Connected to MySQL")
            return conn
        except Error as e:
            print(f"MySQL connection failed ({i+1}/{retries}): {e}")
            time.sleep(delay)
    raise Exception("Could not connect to MySQL after several retries")

# Initialize database tables if not exist
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(80) UNIQUE NOT NULL,
        password VARCHAR(200) NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        value VARCHAR(100)
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

init_db()

# ------------------- AUTH ROUTES -------------------

# Signup
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        conn.close()
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "User created successfully"}), 201

# Login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid username or password"}), 401

    expires = datetime.timedelta(hours=1)
    access_token = create_access_token(identity=str(user["id"]), expires_delta=expires)
    return jsonify({"access_token": access_token}), 200

# ------------------- CRUD ROUTES -------------------

# Create Item
@app.route("/items", methods=["POST"])
@jwt_required()
def create_item():
    user_id = get_jwt_identity()
    data = request.get_json()
    name = data.get("name")
    value = data.get("value")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO items (name, value) VALUES (%s, %s)", (name, value))
    conn.commit()
    item_id = cursor.lastrowid
    cursor.execute("SELECT * FROM items WHERE id=%s", (item_id,))
    item = cursor.fetchone()

    cursor.close()
    conn.close()
    return jsonify(item), 201

# Get All Items
@app.route("/items", methods=["GET"])
@jwt_required()
def get_items():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(items)

# Get One Item
@app.route("/items/<int:item_id>", methods=["GET"])
@jwt_required()
def get_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items WHERE id=%s", (item_id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)

# Update Item
@app.route("/items/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_item(item_id):
    data = request.get_json()
    name = data.get("name")
    value = data.get("value")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items WHERE id=%s", (item_id,))
    item = cursor.fetchone()
    if not item:
        cursor.close()
        conn.close()
        return jsonify({"error": "Item not found"}), 404

    cursor.execute(
        "UPDATE items SET name=%s, value=%s WHERE id=%s",
        (name or item["name"], value or item["value"], item_id)
    )
    conn.commit()
    cursor.execute("SELECT * FROM items WHERE id=%s", (item_id,))
    updated_item = cursor.fetchone()

    cursor.close()
    conn.close()
    return jsonify(updated_item)

# Delete Item
@app.route("/items/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items WHERE id=%s", (item_id,))
    item = cursor.fetchone()
    if not item:
        cursor.close()
        conn.close()
        return jsonify({"error": "Item not found"}), 404

    cursor.execute("DELETE FROM items WHERE id=%s", (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(item)

# ------------------- RUN APP -------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
