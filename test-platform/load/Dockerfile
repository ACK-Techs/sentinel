FROM python:3.11-slim

WORKDIR /app

RUN useradd -u 10001 -m appuser \
  && pip install --no-cache-dir locust==2.31.8

COPY load /app

USER 10001

CMD ["locust", "-f", "locustfile.py", "--headless", "-u", "10", "-r", "2", "--host", "http://gateway:8080"]

