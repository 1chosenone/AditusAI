import logging
import os
from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load variables from .env file
load_dotenv()


class Settings(BaseSettings):

    # Database config
    database_url: str

    # Logging config
    log_level: str = "INFO"

    # LLM config
    anthropic_api_key: SecretStr
    model: str = "cclaude-haiku-4-5-20251001"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Create a single instance to be used across the app
settings = Settings()


def setup_logging():
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
