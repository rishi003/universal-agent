"""Language Model configuration and initialization.

This module handles the setup and configuration of the language model
used by all agents in the application.
"""

from llama_index.llms.openai import OpenAI
from app.core import CONFIG
import logging


__all__ = ["llm", "get_llm"]


logger = logging.getLogger(__name__)


def get_llm() -> OpenAI:
    """Get a configured LLM instance.

    Returns:
        Configured LlamaIndex OpenAI LLM instance using OpenRouter

    Raises:
        ValueError: If required configuration is missing
    """
    try:
        if not CONFIG.openrouter_api_key:
            raise ValueError("OpenRouter API key is required")

        return OpenAI(
            model=CONFIG.model_name,
            api_key=CONFIG.openrouter_api_key,
            api_base=CONFIG.openrouter_base_url,
            temperature=CONFIG.temperature,
            max_tokens=4096,
        )
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        raise


# Global LLM instance
llm = get_llm()
