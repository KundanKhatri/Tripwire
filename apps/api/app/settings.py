from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.local", extra="ignore")

    azure_openai_endpoint: str = Field(default="", alias="AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key: str = Field(default="", alias="AZURE_OPENAI_API_KEY")
    azure_openai_api_version: str = Field(default="2024-10-21", alias="AZURE_OPENAI_API_VERSION")
    azure_openai_deployment_gpt41: str = Field(default="gpt-4o", alias="AZURE_OPENAI_DEPLOYMENT_GPT41")
    azure_openai_deployment_mini: str = Field(default="gpt-4o-mini", alias="AZURE_OPENAI_DEPLOYMENT_MINI")
    azure_openai_deployment_embed: str = Field(
        default="text-embedding-3-large", alias="AZURE_OPENAI_DEPLOYMENT_EMBED"
    )

    azure_content_safety_endpoint: str = Field(default="", alias="AZURE_CONTENT_SAFETY_ENDPOINT")
    azure_content_safety_key: str = Field(default="", alias="AZURE_CONTENT_SAFETY_KEY")

    postgres_url: str = Field(default="", alias="POSTGRES_URL")
    capability_hmac_secret: str = Field(default="dev-only-do-not-use", alias="CAPABILITY_HMAC_SECRET")

    environment: str = Field(default="local", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    app_insights_connection_string: str = Field(default="", alias="APP_INSIGHTS_CONNECTION_STRING")


@lru_cache
def get_settings() -> Settings:
    return Settings()
