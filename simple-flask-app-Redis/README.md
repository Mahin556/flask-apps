# 📦 Items API (CRUD with cURL)

This document shows how to interact with the **Items API** using `curl` commands.

**DOCKER IMAGE:** `docker pull mahinraza556/flask-app:crud-with-mongodb`

**DOCKER CLI:** 

NETWORK
```docker network create my_network -d bridge```

DATABASE
```
docker run -itd \
  --name redis \
  --network my_network \
  -v redis_data:/data \
  redis:6.0 \
  redis-server --requirepass mysecretpassword

```


APP
```
docker run -p 5000:5000 \
  --network my_network \
  -e REDIS_HOST=redis \
  -e REDIS_PORT=6379 \
  -e REDIS_DB=0 \
  -e REDIS_PASSWORD=mysecretpassword \
  mahinraza556/flask-app:crud-with-redis
```

**ENV FILE(.env):**
```
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=mysecretpassword
```

**DOCKER COMPOSE:** 
`docker compose up -d` 
`docker compose down` 
`docker compose down -v` 

## Base URL (example):

### Create a New Item

**POST** `/items`

```bash
curl -X POST http://localhost:5000/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Apple",
    "value": "Fruit"
  }'
```
Example Response:
```
{
  "id": 1,
  "name": "Apple",
  "value": "Fruit"
}

```

### Get all items

**GET** `/items`

```bash
curl -X GET http://localhost:5000/items
```
Example Response:
```
[
  {
    "id": 1,
    "name": "Apple",
    "value": "Fruit"
  },
  {
    "id": 2,
    "name": "Carrot",
    "value": "Vegetable"
  }
]

```

### Get specific item

**GET** `/items/<item_id>`

```bash
curl -X GET http://localhost:5000/items/1
```
Example Response:
```
{
  "id": 1,
  "name": "Apple",
  "value": "Fruit"
}

```
Example Response (404 Not Found):
```
{
  "error": "Item not found"
}
```

### Update an Item

**PUT** `/items/{id}`

```bash
curl -X PUT http://localhost:5000/items/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Banana"
  }'
```
Example Response (200 OK):
```
{
  "id": 1,
  "name": "Banana",
  "value": "Fruit"
}

```
Example Response (404 Not Found):
```
{
  "error": "Item not found"
}
```

### Delete an Item

**DELETE** `/items/{id}`

```bash
curl -X DELETE http://localhost:5000/items/1
```
Example Response (204 No Content):
```
(no response body)
```
Example Response (404 Not Found):
```
{
  "error": "Item not found"
}
```


