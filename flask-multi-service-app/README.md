# Flask Microservices with MySQL

This project contains **two Flask microservices**:

1. **User Service** → Manages users and API keys.
2. **Item Service** → Manages items, requiring a valid API key from User Service.

Both services store data in **MySQL databases**.

---

## 🔹 Requirements

```txt
flask
flask_sqlalchemy
pymysql
requests
```

---

## 🔹 User Service API

Base URL: `http://localhost:9090`

### 1. Signup → Get API key

```bash
curl -X POST http://localhost:9090/signup \
-H "Content-Type: application/json" \
-d '{"username":"alice"}'
```

**Response:**

```json
{
  "username": "alice",
  "api_key": "YOUR_GENERATED_API_KEY"
}
```

### 2. Validate API key

```bash
curl -X POST http://localhost:9090/validate \
-H "Content-Type: application/json" \
-d '{"api_key":"YOUR_GENERATED_API_KEY"}'
```

**Response:**

```json
{"valid": true}
```

---

## 🔹 Item Service API

Base URL: `http://localhost:8080`
**All endpoints require `X-API-KEY` header.**

### 1. Create item

```bash
curl -X POST http://localhost:8080/items \
-H "Content-Type: application/json" \
-H "X-API-KEY: YOUR_GENERATED_API_KEY" \
-d '{"name":"Laptop","value":"Dell XPS"}'
```

**Response:**

```json
{"id":1,"name":"Laptop","value":"Dell XPS"}
```

### 2. List all items

```bash
curl -X GET http://localhost:8080/items \
-H "X-API-KEY: YOUR_GENERATED_API_KEY"
```

**Response:**

```json
[{"id":1,"name":"Laptop","value":"Dell XPS"}]
```

### 3. Get single item by ID

```bash
curl -X GET http://localhost:8080/items/1 \
-H "X-API-KEY: YOUR_GENERATED_API_KEY"
```

**Response:**

```json
{"id":1,"name":"Laptop","value":"Dell XPS"}
```

### 4. Update item

```bash
curl -X PUT http://localhost:8080/items/1 \
-H "Content-Type: application/json" \
-H "X-API-KEY: YOUR_GENERATED_API_KEY" \
-d '{"name":"Laptop","value":"Dell XPS 2025"}'
```

**Response:**

```json
{"id":1,"name":"Laptop","value":"Dell XPS 2025"}
```

### 5. Delete item

```bash
curl -X DELETE http://localhost:8080/items/1 \
-H "X-API-KEY: YOUR_GENERATED_API_KEY"
```

**Response:**

```json
{"id":1,"name":"Laptop","value":"Dell XPS 2025"}
```

---

## ✅ Summary

* **User Service**: signup → get API key → validate API key
* **Item Service**: CRUD operations using the API key from User Service
