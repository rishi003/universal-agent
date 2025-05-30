"""Core module for the universal agent application.

This module provides the foundational components including
configuration, base classes, types, and factory patterns.
"""

from .config import CONFIG
from .types import AgentProfile, AgentType, AgentResponse
from .base import BaseAgent, BaseAgentConfig, AgentRegistry
from .factory import AgentFactory

__all__ = [
    "CONFIG",
    "AgentProfile",
    "AgentType",
    "AgentResponse",
    "BaseAgent",
    "BaseAgentConfig",
    "AgentRegistry",
    "AgentFactory",
]
