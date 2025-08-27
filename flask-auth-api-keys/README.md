BASE="http://127.0.0.1:5000"

### 1) Signup (create a user + get API key)
```bash
API_KEY=$(curl -s -X POST "$BASE/signup" \
  -H "Content-Type: application/json" \
  -d '{"username":"alice"}' | jq -r .api_key)
echo "API_KEY=$API_KEY"
```

### 2) Create items
```bash
curl -s -X POST "$BASE/items" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{"name":"Book","value":"Python 101"}' | jq

curl -s -X POST "$BASE/items" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{"name":"Laptop","value":"ThinkPad"}' | jq
```

### 3) Get all items
```bash
curl -s "$BASE/items" -H "X-API-KEY: $API_KEY" | jq
```

### 4) Get one item
```bash
curl -s "$BASE/items/1" -H "X-API-KEY: $API_KEY" | jq
```

### 5) Update item
```bash
curl -s -X PUT "$BASE/items/1" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{"value":"Flask 101"}' | jq
```

### 6) Delete item
```bash
curl -s -X DELETE "$BASE/items/2" -H "X-API-KEY: $API_KEY" | jq
```

### 7) Get all items again
```bash
curl -s "$BASE/items" -H "X-API-KEY: $API_KEY" | jq
```

Image --> `mahinraza556/flask-app:flask-auth-api-keys`

Docker run ---> 
```bash
docker run -dit -p 5000:5000 -v $(pwd)/data:/app/instance mahinraza556/flask-app:flask-auth-api-keys
or
docker run -dit -p 5000:5000 -v db_data:/app/instance mahinraza556/flask-app:flask-auth-api-keys
```

Docker compose  ---> 
```bash
docker compose up -d
docker compose up -d --build
docker compose down 
docker compose down -v
```

