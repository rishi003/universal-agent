"""Type definitions for the universal agent application.

This module contains all the custom types, models, and data structures
used throughout the application.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum


__all__ = [
    "AgentProfile",
    "AgentType",
    "AgentResponse",
]


class AgentType(str, Enum):
    """Enumeration of available agent types."""

    IDEATION = "ideation"
    IDEA_ANALYSIS = "idea_analysis"
    MANAGER = "manager"


class AgentProfile(BaseModel):
    """Profile configuration for an agent.

    This model defines the core characteristics and behavior
    of an agent, including its role, objectives, and background.
    """

    role: str = Field(
        ..., description="The primary role or function of the agent", min_length=1
    )
    goal: str = Field(
        ...,
        description="The main objective or goal the agent should achieve",
        min_length=1,
    )
    backstory: str = Field(
        ...,
        description="Background context and behavioral guidelines for the agent",
        min_length=1,
    )


class AgentResponse(BaseModel):
    """Standardized response format from agents.

    This model provides a consistent structure for agent responses,
    including the content, metadata, and any additional context.
    """

    content: str = Field(..., description="The main response content from the agent")
    agent_type: AgentType = Field(
        ..., description="The type of agent that generated this response"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata about the response"
    )
    success: bool = Field(
        default=True, description="Whether the agent execution was successful"
    )
    error_message: Optional[str] = Field(
        default=None, description="Error message if the execution failed"
    )
