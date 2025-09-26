FROM python:3.9-slim

WORKDIR /app

COPY app.py requirements.txt /app/

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
