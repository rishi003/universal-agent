"""Agent module initialization.

This module exports the main agents used in the application.
"""

from .workflow import universal_workflow, UniversalAgentWorkflow
from .base_implementation import create_agent

__all__ = [
    "universal_workflow",
    "UniversalAgentWorkflow",
]

# Import agent profiles
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

# Individual agent workflows for direct invocation
ideation_workflow = create_agent(ideation_agent_profile)
idea_analysis_workflow = create_agent(idea_analysis_agent_profile)
product_manager_workflow = create_agent(product_manager_agent_profile)
strategic_advisor_workflow = create_agent(strategic_advisor_agent_profile)
landing_page_workflow = create_agent(landing_page_designer_agent_profile)
cto_workflow = create_agent(cto_agent_profile)
advertising_strategist_workflow = create_agent(advertising_strategist_agent_profile)

agent_workflows = {
    "ideation": ideation_workflow,
    "ideaanalysis": idea_analysis_workflow,
    "productmanager": product_manager_workflow,
    "strategicadvisor": strategic_advisor_workflow,
    "landingpage": landing_page_workflow,
    "cto": cto_workflow,
    "advertisingstrategist": advertising_strategist_workflow,
}

__all__.extend([
    "agent_workflows",
    "ideation_workflow",
    "idea_analysis_workflow",
    "product_manager_workflow",
    "strategic_advisor_workflow",
    "landing_page_workflow",
    "cto_workflow",
    "advertising_strategist_workflow",
])
