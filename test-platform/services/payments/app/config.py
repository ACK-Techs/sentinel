from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    service_name: str = "payments"
    service_version: str = "0.1.0"
    deployment_env: str = "dev"
    db_url: str
    redis_url: str
    chaos_token: str = "sentinel-chaos-token"
    otel_exporter_otlp_endpoint: str


settings = Settings()  # type: ignore[call-arg]
