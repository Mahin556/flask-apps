# Flask JWT + MySQL API

This is a Flask application with JWT authentication and MySQL database using cursor-based connections. It supports user signup/login and CRUD operations on items.

---

## **Environment Variables**

| Variable       | Description                   | Default          |
|----------------|-------------------------------|----------------|
| DB_USER        | MySQL username                | mahin          |
| DB_PASSWORD    | MySQL password                | mahin          |
| DB_HOST        | MySQL host                    | mysql          |
| DB_NAME        | MySQL database                | flask_crud     |
| JWT_SECRET_KEY | Secret key for JWT tokens     | supersecretkey |

---

## **Endpoints**

### **1. Signup**

**POST** `/signup`

Request body:

```json
{
  "username": "testuser",
  "password": "password123"
}
```

Curl:

```bash
curl -X POST http://localhost:5000/signup -H "Content-Type: application/json" -d '{"username": "testuser", "password": "password123"}'
```

---

### **2. Login**

**POST** `/login`

Request body:

```json
{
  "username": "testuser",
  "password": "password123"
}
```

Curl:

```bash
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username": "testuser", "password": "password123"}'
```

Response:

```json
{
  "access_token": "<JWT_TOKEN>"
}
```

> Use this token for all protected endpoints.

---

## **Protected Item Endpoints**

**Header required:**

```
Authorization: Bearer <JWT_TOKEN>
```

### **3. Create Item**

**POST** `/items`

Request body:

```json
{
  "name": "Apple",
  "value": "Fruit"
}
```

Curl:

```bash
curl -X POST http://localhost:5000/items -H "Authorization: Bearer <JWT_TOKEN>" -H "Content-Type: application/json" -d '{"name": "Apple", "value": "Fruit"}'
```

---

### **4. Get All Items**

**GET** `/items`

Curl:

```bash
curl -H "Authorization: Bearer <JWT_TOKEN>" http://localhost:5000/items
```

---

### **5. Get One Item**

**GET** `/items/<item_id>`

Curl:

```bash
curl -H "Authorization: Bearer <JWT_TOKEN>" http://localhost:5000/items/1
```

---

### **6. Update Item**

**PUT** `/items/<item_id>`

Request body:

```json
{
  "name": "Banana",
  "value": "Fruit"
}
```

Curl:

```bash
curl -X PUT http://localhost:5000/items/1 -H "Authorization: Bearer <JWT_TOKEN>" -H "Content-Type: application/json" -d '{"name": "Banana", "value": "Fruit"}'
```

---

### **7. Delete Item**

**DELETE** `/items/<item_id>`

Curl:

```bash
curl -X DELETE http://localhost:5000/items/1 -H "Authorization: Bearer <JWT_TOKEN>"
```

> Notes:
> - Replace `<JWT_TOKEN>` with the token received from `/login`.
> - All item routes are protected and require a valid JWT token.
> - Use the retry logic in the Flask app to ensure MySQL is ready when the container starts.

---

## **Docker Compose**

To start MySQL and Flask together:

```bash
docker-compose up --build
```

Ensure `.env` file has all required environment variables.

---

## **Optional: `.env` Example**

```env
DB_USER=mahin
DB_PASSWORD=mahin
DB_HOST=mysql
DB_NAME=flask_crud
JWT_SECRET_KEY=supersecretkey
```

Clone the repo, create `.env` using the above template, and run `docker-compose up --build` to start the app immediately.
