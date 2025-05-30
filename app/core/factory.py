"""
Factory pattern implementation for creating agents.

This module provides factory classes and functions for creating
agent instances in a consistent and configurable way.
"""

from typing import Type, Dict, Any
from .base import BaseAgent, BaseAgentConfig
from .types import AgentProfile


class AgentFactory:
    """
    Factory class for creating agent instances.

    This factory provides a centralized way to create agents
    with consistent configuration and initialization patterns.
    """

    _agent_classes: Dict[str, Type[BaseAgent]] = {}

    @classmethod
    def register_agent_class(cls, name: str, agent_class: Type[BaseAgent]) -> None:
        """
        Register an agent class with the factory.

        Args:
            name: Unique identifier for the agent class
            agent_class: The agent class to register
        """
        cls._agent_classes[name] = agent_class

    @classmethod
    def create_agent(
        cls, agent_type: str, profile: AgentProfile, llm: Any, **kwargs: Any
    ) -> BaseAgent:
        """
        Create an agent instance of the specified type.

        Args:
            agent_type: The type of agent to create
            profile: The agent profile configuration
            llm: The language model instance
            **kwargs: Additional configuration parameters

        Returns:
            Configured agent instance

        Raises:
            ValueError: If the agent type is not registered
        """
        if agent_type not in cls._agent_classes:
            raise ValueError(f"Unknown agent type: {agent_type}")

        agent_class = cls._agent_classes[agent_type]
        config = BaseAgentConfig(profile=profile, llm=llm, **kwargs)
        return agent_class(config)

    @classmethod
    def get_registered_types(cls) -> list[str]:
        """
        Get a list of all registered agent types.

        Returns:
            List of registered agent type names
        """
        return list(cls._agent_classes.keys())

    @classmethod
    def is_registered(cls, agent_type: str) -> bool:
        """
        Check if an agent type is registered.

        Args:
            agent_type: The agent type to check

        Returns:
            True if the agent type is registered, False otherwise
        """
        return agent_type in cls._agent_classes
