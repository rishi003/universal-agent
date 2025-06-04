"""
Base classes and interfaces for the universal agent application.

This module provides the foundational classes and patterns used throughout
the application, including base agent classes and common interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic_ai import Agent
from pydantic import BaseModel

from .types import AgentProfile


class BaseAgentConfig(BaseModel):
    """
    Configuration model for agent creation.

    This class defines the standard configuration parameters
    that all agents should support.
    """

    profile: AgentProfile
    llm: Any


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.

    This class provides a common interface and shared functionality
    for all agent implementations, promoting consistency and
    reducing code duplication.
    """

    def __init__(self, config: BaseAgentConfig):
        """
        Initialize the base agent with configuration.

        Args:
            config: The agent configuration containing profile and settings
        """
        self.config = config
        self._agent = self._create_agent()

    def _create_agent(self) -> Agent:
        """
        Create the underlying PydanticAI Agent instance.

        Returns:
            Configured PydanticAI Agent instance
        """
        return Agent(
            model=self.config.llm,
            system_prompt=self.config.profile.backstory,
        )

    @property
    def agent(self) -> Agent:
        """Get the underlying PydanticAI Agent instance."""
        return self._agent

    @abstractmethod
    def kickoff(self, input_data: str) -> Any:
        """
        Execute the agent's main functionality.

        Args:
            input_data: The input data for the agent to process

        Returns:
            The agent's response or result
        """
        pass

    def __getattr__(self, name: str) -> Any:
        """
        Delegate attribute access to the underlying agent.

        This allows the BaseAgent to act as a proxy to the PydanticAI Agent,
        maintaining backward compatibility while adding our abstractions.
        """
        return getattr(self._agent, name)


class AgentRegistry:
    """
    Registry for managing agent instances and their configurations.

    This class provides a centralized way to register, retrieve,
    and manage different agent types in the application.
    """

    _agents: Dict[str, BaseAgent] = {}
    _profiles: Dict[str, AgentProfile] = {}

    @classmethod
    def register_agent(cls, name: str, agent: BaseAgent) -> None:
        """
        Register an agent instance.

        Args:
            name: Unique identifier for the agent
            agent: The agent instance to register
        """
        cls._agents[name] = agent

    @classmethod
    def register_profile(cls, name: str, profile: AgentProfile) -> None:
        """
        Register an agent profile.

        Args:
            name: Unique identifier for the profile
            profile: The agent profile to register
        """
        cls._profiles[name] = profile

    @classmethod
    def get_agent(cls, name: str) -> Optional[BaseAgent]:
        """
        Retrieve a registered agent.

        Args:
            name: The agent identifier

        Returns:
            The agent instance if found, None otherwise
        """
        return cls._agents.get(name)

    @classmethod
    def get_profile(cls, name: str) -> Optional[AgentProfile]:
        """
        Retrieve a registered profile.

        Args:
            name: The profile identifier

        Returns:
            The agent profile if found, None otherwise
        """
        return cls._profiles.get(name)

    @classmethod
    def list_agents(cls) -> list[str]:
        """Get a list of all registered agent names."""
        return list(cls._agents.keys())

    @classmethod
    def list_profiles(cls) -> list[str]:
        """Get a list of all registered profile names."""
        return list(cls._profiles.keys())
