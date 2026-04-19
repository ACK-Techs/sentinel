FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd -u 10001 -m appuser

COPY libs/observability /tmp/observability
RUN pip install --no-cache-dir /tmp/observability

COPY services/gateway /app
RUN pip install --no-cache-dir .

USER 10001
EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

