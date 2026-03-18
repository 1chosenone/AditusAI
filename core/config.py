"""Configuration management for AditusAI application.

This module provides settings management using Pydantic BaseSettings,
loading configuration from environment variables and .env files.
"""

import logging
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        database_url: Database connection URL.
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        anthropic_api_key: API key for Anthropic LLM service.
        model: Model identifier for the LLM.
    """

    # Database config
    database_url: str

    # Logging config
    log_level: str = "INFO"

    # LLM config
    anthropic_api_key: SecretStr
    llm_model_name: str = "claude-haiku-4-5-20251001"
    llm_temperature: float = 0.3
    llm_max_tokens: int = 10_000
    llm_max_tries: int = 3

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Create a single instance to be used across the app
settings = Settings()


def setup_logging():
    """Configure application logging with settings from the environment."""
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
