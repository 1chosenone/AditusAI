"""Configuration management for AditusAI application.

This module provides settings management using Pydantic BaseSettings,
loading configuration from environment variables and .env files.
"""

import logging
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMTaskConfig(BaseModel):
    """Configuration for LLM task execution.

    Attributes:
        model: Model identifier for the LLM.
        temperature: Sampling temperature (default: 0.3).
        max_tokens: Maximum tokens in the response (default: 10,000).
        max_tries: Maximum number of retry attempts (default: 3).
        api_base: API base URL for Ollama (default: None).
    """

    model: str
    temperature: float = 0.3
    max_tokens: int = 10_000
    max_tries: int = 3
    api_base: str | None = None


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        database_url: Database connection URL.
        redis_url: Redis connection URL.
        n8n_job_search_webhook_url: Webhook URL for n8n job search.
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        anthropic_api_key: API key for Anthropic LLM service.
        openai_api_key: API key for OpenAI LLM service.
        ollama_api_base: API base URL for Ollama.
        llm_resume_parsing_model: Model for resume parsing.
        llm_query_optimization_model: Model for query optimization.
        llm_query_parsing_model: Model for query parsing.
        llm_query_inference_model: Model for query inference from skills.
    """

    # Database config
    database_url: str

    # Redis config
    redis_url: str

    # n8n webhooks
    n8n_job_search_webhook_url: str

    # Logging config
    log_level: str = "DEBUG"

    # LLM config
    anthropic_api_key: SecretStr | None = None
    openai_api_key: SecretStr | None = None
    ollama_api_base: str | None = None

    # Models
    llm_resume_parsing_model: str = "anthropic/claude-haiku-4-5-20251001"
    llm_query_optimization_model: str = "openai/gpt-4o"
    llm_query_parsing_model: str = "ollama/llama3"
    llm_query_inference_model: str = "ollama/llama3"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def parsing_llm(self) -> LLMTaskConfig:
        """Get LLM config for resume parsing."""
        return LLMTaskConfig(model=self.llm_resume_parsing_model)

    @property
    def query_optimization_llm(self) -> LLMTaskConfig:
        """Get LLM config for query optimization."""
        return LLMTaskConfig(
            model=self.llm_query_optimization_model,
            temperature=0.4,
            max_tokens=250,
            api_base=self.ollama_api_base,
        )

    @property
    def query_parsing_llm(self) -> LLMTaskConfig:
        """Get LLM config for query parsing."""
        return LLMTaskConfig(
            model=self.llm_query_parsing_model,
            temperature=0.0,
            max_tokens=100,
            max_tries=1,
        )

    @property
    def query_inference_llm(self) -> LLMTaskConfig:
        """Get LLM config for query inference from skills."""
        return LLMTaskConfig(
            model=self.llm_query_inference_model,
            temperature=0.3,
            max_tokens=250,
            max_tries=2,
        )


# Create a single instance to be used across the app
settings = Settings()


def setup_logging():
    """Configure application logging with settings from the environment."""
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
