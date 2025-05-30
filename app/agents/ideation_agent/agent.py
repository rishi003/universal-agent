"""Ideation Agent implementation.

This module contains the IdeationAgent that specializes in
generating and refining innovative ideas through recursive thinking.
"""

from ..base_implementation import create_agent
from .profile import ideation_agent_profile


__all__ = ["IdeationAgent"]


# Create the IdeationAgent using the factory function
IdeationAgent = create_agent(ideation_agent_profile)
