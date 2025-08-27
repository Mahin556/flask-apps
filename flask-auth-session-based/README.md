Got it 👍 — here’s a **single bash command** you can run to create a `README.md` file with the detailed session-based authentication version:

````bash
cat > README.md << 'EOF'
# 📦 Items API (CRUD with Session-Based Authentication & Docker)

This repository demonstrates a **Flask-based Items API** with authentication, containerized using Docker.  
It supports **CRUD operations** on items, secured with **Session-based authentication (Flask-Login + Cookies)**.

---

## 🚀 Docker Setup

### 🔹 Pull Docker Image

```bash
docker pull mahinraza556/flask-app:flask-auth-session-based
````

### 🔹 Create Network

```bash
docker network create my_network -d bridge
```

### 🔹 Run PostgreSQL Database

```bash
docker run -itd \
  --name=postgresql \
  --network=my_network \
  -v db_data:/var/lib/postgresql/data \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=root \
  -e POSTGRES_DB=flask_crud \
  postgres:15
```

### 🔹 Run Flask App

```bash
docker run -p 5000:5000 \
  --network=my_network \
  -e DB_USER=root \
  -e DB_PASSWORD=root \
  -e DB_HOST=postgresql \
  -e DB_NAME=flask_crud \
  mahinraza556/flask-app:flask-auth-session-based
```

---

## ⚙️ Environment Variables (.env)

```env
DB_USER=<user>
DB_PASSWORD=<user_password>
DB_HOST=<host>
DB_NAME=<db_name>
DB_ROOT_PASSWORD=<root_password>
```

---

## 🐳 Docker Compose

```bash
docker compose up -d
docker compose down
docker compose down -v   # also removes volumes
```

---

## 🌐 API Reference

Base URL: `http://localhost:5000`

### 🔹 Authentication (Session-Based)

Unlike JWT, session-based authentication uses **cookies** managed by Flask.
When you log in successfully, Flask sets a **session cookie** (`session=<encrypted_value>`) in your browser or `curl`.
This cookie must be sent with all subsequent requests to access protected routes.

---

#### 1. Signup

**POST** `/signup`

```bash
curl -X POST http://localhost:5000/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

---

#### 2. Login

**POST** `/login`

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"username": "testuser", "password": "password123"}'
```

✅ Note:

* The `-c cookies.txt` flag saves the session cookie in a file.
* This cookie will be reused for protected endpoints.

---

#### 3. Logout

**GET** `/logout`

```bash
curl -X GET http://localhost:5000/logout -b cookies.txt
```

---

### 🔹 Items Endpoints (Protected)

All these endpoints require being logged in. Use `-b cookies.txt` with each request.

#### Create Item

**POST** `/items`

```bash
curl -X POST http://localhost:5000/items \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"name": "Apple", "value": "Fruit"}'
```

#### Get All Items

**GET** `/items`

```bash
curl -b cookies.txt http://localhost:5000/items
```

#### Get One Item

**GET** `/items/<item_id>`

```bash
curl -b cookies.txt http://localhost:5000/items/1
```

#### Update Item

**PUT** `/items/<item_id>`

```bash
curl -X PUT http://localhost:5000/items/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"name": "Banana", "value": "Fruit"}'
```

#### Delete Item

**DELETE** `/items/<item_id>`

```bash
curl -X DELETE http://localhost:5000/items/1 -b cookies.txt
```

---

## ✅ Example Workflow

1. Signup a new user
2. Login → cookie gets stored in `cookies.txt`
3. Use `-b cookies.txt` for CRUD operations on items
4. Logout to end session

---

## 📌 Example Responses

**Create Item**

```json
{
  "id": 1,
  "name": "Apple",
  "value": "Fruit"
}
```

**Get All Items**

```json
[
  { "id": 1, "name": "Apple", "value": "Fruit" },
  { "id": 2, "name": "Carrot", "value": "Vegetable" }
]
```

**Item Not Found**

```json
{ "error": "Item not found" }
```

---

## 🛠️ Tech Stack

* **Flask** (Python API)
* **PostgreSQL** (Database)
* **Session-Based Authentication (Flask-Login + Cookies)**
* **Docker & Docker Compose**

---

📌 Author: *Mahin Raza*
EOF

```

Run this whole command in your terminal, and it will create a ready-to-use `README.md` file. ✅  

Do you also want me to include a **diagram of how session cookies flow** (login → session → protected routes → logout) inside the README?
```





# Flask-Login and Session Cookies Explained

## 🔹 1. App & Config Initialization

- `app = Flask(__name__)` → Creates the Flask web application.
- `app.config[...]` → Configures the app with:
  - `SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"` → Uses SQLite as the database.
  - `SECRET_KEY` → Needed for securely signing session cookies (Flask-Login uses this).
  - `SQLALCHEMY_TRACK_MODIFICATIONS = False` → Disables event notifications (saves resources).
- `db = SQLAlchemy(app)` → Connects SQLAlchemy ORM to Flask.
- `bcrypt = Bcrypt(app)` → For hashing passwords securely.
- `login_manager = LoginManager(app)` → Manages user sessions (login/logout).

---

## 🔹 2. Models (Database Tables)

### User model:
- Inherits `UserMixin` → Gives it Flask-Login features (`is_authenticated`, `is_active`, etc.).
- Stores `username` and a hashed `password`.

### Item model:
- Simple table with `id`, `name`, and `value`.
- Has a helper `.to_dict()` to return JSON-ready data.

- `db.create_all()` → Creates the SQLite tables (`users.db`) if not already present.

---

## 🔹 3. Flask-Login User Loader
```python
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```
- When Flask-Login needs to check "who is the current user?" (e.g., for `@login_required`), it calls this function.
- It loads the `User` object from the database by its `id`.

---

## 🔹 4. Authentication

### Signup
- Client sends `POST /signup` with `{username, password}`.
- The server:
  - Checks if user exists.
  - Hashes password with `bcrypt.generate_password_hash()`.
  - Saves new user in DB.
- Returns **201 Created**.

### Login
- Client sends `POST /login` with `{username, password}`.
- The server:
  - Fetches user from DB.
  - Checks password with `bcrypt.check_password_hash()`.
  - If valid → Calls `login_user(user)`.
  - This stores the user's ID in Flask's session cookie (signed with `SECRET_KEY`).
- From now on, every request will carry that session cookie.

### Logout
- Client calls `GET /logout`.
- The server calls `logout_user()`, which clears the session cookie.

---

## 🔹 5. Session & Security

- Flask-Login uses **secure session cookies** to track logged-in users.
- Each request:
  - Reads the cookie.
  - Uses `load_user(user_id)` to fetch the user from DB.
  - Populates `current_user` (available anywhere in Flask).
- If a user isn’t logged in, `@login_required` will redirect them to `/login`.

---

## 🔹 6. CRUD Operations (Protected)

- All CRUD routes are decorated with `@login_required`, so only authenticated users can access them.

- **Create Item (POST /items)** → Creates a new row in the `items` table.
- **Get All Items (GET /items)** → Returns a list of all items in JSON.
- **Get One Item (GET /items/<id>)** → Fetches one item by `id`.
- **Update Item (PUT /items/<id>)** → Modifies existing `name`/`value`.
- **Delete Item (DELETE /items/<id>)** → Deletes the row and returns deleted object.

---

## 🔹 7. Behind the Scenes Flow

1. User signs up → Password hashed → Saved in DB.
2. User logs in → Session cookie created with `login_user`.
3. On every request:
   - Flask reads cookie.
   - Uses `load_user()` to get user object.
   - Sets `current_user`.
4. Protected routes (`@login_required`) → Check if `current_user.is_authenticated`.
   - If yes → Request continues.
   - If no → Redirect to login page.
5. Logout clears session → User must log in again.

---

## 🔹 How `login_user` and `logout_user` Work Internally

### `login_user(user)`
- Stores user ID in session:  
  ```python
  session["_user_id"] = str(user.get_id())
  session["_fresh"] = True
  ```
- Flask signs session cookie with `SECRET_KEY`.
- Browser stores cookie, sends it with every request.

### Request Processing
- Cookie received in request headers.
- Flask verifies signature and loads `_user_id`.
- Calls `@login_manager.user_loader` to fetch user from DB.
- Sets `current_user`.

### `logout_user()`
- Clears session keys:
  ```python
  session.pop("_user_id", None)
  session.pop("_fresh", None)
  ```
- Browser overwrites cookie → user logged out.

---

## 🔹 Flask Session Cookie Internals

1. **Session Creation**
   ```python
   session["username"] = "mahin"
   ```
   - Flask serializes dict into JSON-like string.
   - Signs with `SECRET_KEY`.

2. **Cookie Storage**
   - Sent as `Set-Cookie` header.
   - Browser saves it.

3. **Validation**
   - On next request, cookie sent back.
   - Flask verifies signature.
   - If valid → loads data back into `session` dict.

4. **Flask-Login’s Usage**
   - Stores `_user_id` in session.
   - Uses it to restore `current_user` each request.

---

## 🔹 Security Features
- **Signing (HMAC)** → prevents tampering.
- **HttpOnly** → prevents JavaScript access.
- **Secure** → only over HTTPS.
- **SameSite** → helps prevent CSRF.

---

## ✅ In Short
- Flask session = signed cookie.
- `SECRET_KEY` ensures safety.
- Flask-Login stores `_user_id` inside.
- Each request verifies cookie → restores user → enforces `@login_required`.
