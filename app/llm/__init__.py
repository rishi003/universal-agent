"""Language Model module for the universal agent application.

This module provides language model instances and utilities
for agent communication and processing.
"""

from .llm import llm, get_llm

__all__ = ["llm", "get_llm"]
