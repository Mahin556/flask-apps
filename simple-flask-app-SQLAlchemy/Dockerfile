FROM python:3.11.13-slim

LABEL description="Basic flask app to demonstrate CRUD operations." \
        version="1.0" \
        maintainer="Mahin Raza mahinraza556@gmail.com"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]