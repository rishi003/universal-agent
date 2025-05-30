"""Language Model configuration and initialization.

This module handles the setup and configuration of the language model
used by all agents in the application.
"""

from crewai import LLM
from app.core import CONFIG
import logging


__all__ = ["llm", "get_llm"]


logger = logging.getLogger(__name__)


def get_llm() -> LLM:
    """Get a configured LLM instance.

    Returns:
        Configured CrewAI LLM instance

    Raises:
        ValueError: If required configuration is missing
    """
    try:
        if not CONFIG.openrouter_api_key:
            raise ValueError("OpenRouter API key is required")

        if not CONFIG.openrouter_base_url:
            raise ValueError("OpenRouter base URL is required")

        return LLM(
            model="openrouter/openai/gpt-4.1",
            base_url=CONFIG.openrouter_base_url,
            api_key=CONFIG.openrouter_api_key,
        )
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        raise


# Global LLM instance
llm = get_llm()
