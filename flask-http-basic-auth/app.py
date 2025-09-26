from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# In-memory users (username → password)
users = {
    "admin": "secret",
    "mahin": "mahin123"
}

# Authentication check
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    return None

# Protected route
@app.route("/secure-data")
@auth.login_required
def get_secure_data():
    return jsonify({"message": f"Hello, {auth.current_user()}! This is protected data."})

# Public route
@app.route("/")
def index():
    return jsonify({"message": "Welcome! Use /secure-data with authentication."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
