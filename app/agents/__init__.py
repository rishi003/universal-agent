"""Agent module initialization.

This module exports the unified agent workflow using PydanticAI.
"""

from .workflow import agent_workflow, AgentWorkflow

__all__ = [
    "agent_workflow",
    "AgentWorkflow",
]

# Import agent profiles for reference
from .ideation_agent.profile import ideation_agent_profile
from .idea_analysis_agent.profile import idea_analysis_agent_profile
from .manager_agent.profile import manager_agent_profile
from .product_manager_agent.profile import product_manager_agent_profile
from .strategic_advisor_agent.profile import strategic_advisor_agent_profile
from .landing_page_designer_agent.profile import landing_page_designer_agent_profile
from .cto_agent.profile import cto_agent_profile
from .advertising_strategist_agent.profile import advertising_strategist_agent_profile

# Add agent profiles to __all__
__all__.extend(
    [
        "ideation_agent_profile",
        "idea_analysis_agent_profile",
        "manager_agent_profile",
        "product_manager_agent_profile",
        "strategic_advisor_agent_profile",
        "landing_page_designer_agent_profile",
        "cto_agent_profile",
        "advertising_strategist_agent_profile",
    ]
)
