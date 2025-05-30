"""Base implementation utilities for agents.

This module provides utility functions and patterns for creating
agents consistently across the application.
"""

from crewai import Agent
from app.core.types import AgentProfile
from app.llm import llm
from typing import Any


def create_agent(profile: AgentProfile, llm_instance: Any = None) -> Agent:
    """
    Create a CrewAI Agent with the given profile.

    This function provides a consistent way to create agents
    while reducing code duplication across agent modules.

    Args:
        profile: The agent profile containing role, goal, and backstory
        llm_instance: Optional LLM instance. If not provided, uses default llm

    Returns:
        Configured CrewAI Agent instance
    """
    if llm_instance is None:
        llm_instance = llm

    return Agent(
        role=profile.role,
        goal=profile.goal,
        backstory=profile.backstory,
        llm=llm_instance,
    )


__all__ = ["create_agent"]
