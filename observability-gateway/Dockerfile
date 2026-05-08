FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

RUN python -m pip install --upgrade pip build

COPY pyproject.toml ./
COPY src ./src

RUN printf '# sentinel-observability-gateway\n' > README.md
RUN python -m build --wheel

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends wget ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 10001 sentinel \
    && useradd --uid 10001 --gid 10001 --create-home --shell /usr/sbin/nologin sentinel

WORKDIR /app

COPY --from=builder /build/dist/*.whl /tmp/
RUN python -m pip install --upgrade pip \
    && python -m pip install /tmp/*.whl \
    && rm -f /tmp/*.whl

USER sentinel

EXPOSE 8091

CMD ["sentinel-observability-gateway"]
