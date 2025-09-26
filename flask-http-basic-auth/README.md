### Docker 
```
docker pull mahinraza556/flask-app:flask-http-basic-auth
docker run -d -p 5000:5000 mahinraza556/flask-app:flask-http-basic-auth
```

### 🧪 Test with `curl`

✅ Access **without authentication**:

```bash
curl http://127.0.0.1:5000/
```

Output:

```json
{"message":"Welcome! Use /secure-data with authentication."}
```

❌ Access **protected route without auth**:

```bash
curl http://127.0.0.1:5000/secure-data
```

Output:

```
Unauthorized Access
```

✅ Access **with valid credentials**:

```bash
curl -u admin:secret http://127.0.0.1:5000/secure-data
```

Output:

```json
{"message":"Hello, admin! This is protected data."}
```
