from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    service_name: str = "worker"
    service_version: str = "0.1.0"
    deployment_env: str = "dev"
    redis_url: str
    orders_stream: str = "orders.events"
    consumer_group: str = "orders-workers"
    consumer_name: str = "worker-1"
    chaos_token: str = "sentinel-chaos-token"
    otel_exporter_otlp_endpoint: str


settings = Settings()  # type: ignore[call-arg]
