from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


__all__ = ["CONFIG"]


class Config(BaseSettings):
    """
    Configuration settings for the application.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    model_name: str = Field(
        default="gpt-4.1",
        description="The name of the OpenAI model to use for generating responses.",
    )
    temperature: float = Field(
        default=0.1,
        description="Sampling temperature for the OpenAI model.",
    )
    openai_api_key: str = Field(
        description="The API key for accessing OpenAI services.",
        alias="OPENAI_API_KEY",
    )
    openai_api_base: str = Field(
        description="The base URL for the OpenAI API.",
        alias="OPENROUTER_BASE_URL",
    )
    openrouter_api_key: str = Field(
        description="The API key for accessing OpenRouter services.",
        alias="OPENROUTER_API_KEY",
    )
    openrouter_base_url: str = Field(
        default="https://api.openrouter.ai/v1",
        description="The base URL for the OpenRouter API.",
    )


CONFIG = Config()
