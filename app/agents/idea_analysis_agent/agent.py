"""Idea Analysis Agent implementation.

This module contains the IdeaAnalysisAgent that specializes in
evaluating, optimizing, and ranking business ideas.
"""

from ..base_implementation import create_agent
from .profile import idea_analysis_agent_profile


__all__ = ["IdeaAnalysisAgent"]


# Create the IdeaAnalysisAgent using the factory function
IdeaAnalysisAgent = create_agent(idea_analysis_agent_profile)
