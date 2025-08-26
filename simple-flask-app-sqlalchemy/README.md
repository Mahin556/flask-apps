# 📦 Items API (CRUD with cURL)

This document shows how to interact with the **Items API** using `curl` commands.

**DOCKER IMAGE:** `docker pull mahinraza556/flask-app:crud-with-sqlalchemyDB`

**DOCKER RUN:** `docker run -itd -p 5000:5000 -v $(pwd)/data:/app/instance mahinraza556/flask-app:crud-with-sqlalchemyDB`

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


