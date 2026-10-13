from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Amidzi"
    app_env: str = "development"
    cors_origins: str = "http://localhost:3000"
    database_url: str = "sqlite:///./dashboard.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
