"""Language Model configuration and initialization.

This module handles the setup and configuration of the language model
used by all agents in the application using PydanticAI.
"""

from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openrouter import OpenRouterProvider
from app.core import CONFIG
import logging


__all__ = ["get_model", "model"]


logger = logging.getLogger(__name__)


def get_model() -> OpenAIModel:
    """Get a configured PydanticAI model instance.

    Returns:
        Configured PydanticAI OpenAIModel using OpenRouter

    Raises:
        ValueError: If required configuration is missing
    """
    try:
        if not CONFIG.openrouter_api_key:
            raise ValueError("OpenRouter API key is required")

        return OpenAIModel(
            CONFIG.model_name,
            provider=OpenRouterProvider(api_key=CONFIG.openrouter_api_key),
        )
    except Exception as e:
        logger.error(f"Failed to initialize model: {e}")
        raise


# Global model instance
model = get_model()
