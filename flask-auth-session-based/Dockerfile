FROM python:3.11.13-slim

LABEL description="Basic flask app to demonstrate CRUD operations with PostgreSQL database and use session based auth" \
        version="1.3" \
        maintainer="Mahin Raza mahinraza556@gmail.com"

ENV FLASK_APP=app.py

# Unbuffered Python output (helps logging in Docker):
ENV PYTHONUNBUFFERED=1 

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["flask"]
CMD ["run", "--host", "0.0.0.0"]