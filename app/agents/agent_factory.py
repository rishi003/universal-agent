"""Agent factory module for creating all agents in the workflow."""

from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.llms import LLM
from typing import List, Callable
from app.agents.ideation_agent.profile import ideation_agent_profile
from app.agents.idea_analysis_agent.profile import idea_analysis_agent_profile
from app.agents.manager_agent.profile import manager_agent_profile
from app.agents.product_manager_agent.profile import product_manager_agent_profile
from app.agents.strategic_advisor_agent.profile import strategic_advisor_agent_profile
from app.agents.landing_page_designer_agent.profile import (
    landing_page_designer_agent_profile,
)
from app.agents.cto_agent.profile import cto_agent_profile
from app.agents.advertising_strategist_agent.profile import (
    advertising_strategist_agent_profile,
)


def create_agents(llm: LLM, tools: List[Callable]) -> List[FunctionAgent]:
    """Create all agents for the workflow including the ManagerAgent."""

    # Manager Agent
    manager_agent = FunctionAgent(
        name="ManagerAgent",
        description="Oversees activities, maintains plans, and coordinates between agents.",
        system_prompt=manager_agent_profile.backstory,
        llm=llm,
        tools=tools,
        can_handoff_to=[
            "IdeationAgent",
            "IdeaAnalysisAgent",
            "ProductManagerAgent",
            "StrategicAdvisorAgent",
            "LandingPageDesignerAgent",
            "CTOAgent",
            "AdvertisingStrategistAgent",
        ],
    )

    # Ideation Agent
    ideation_agent = FunctionAgent(
        name="IdeationAgent",
        description="Generates innovative ideas using recursive thinking and creative processes.",
        system_prompt=(
            f"{ideation_agent_profile.backstory} "
            "After your ideation work, hand off control back to the ManagerAgent."
        ),
        llm=llm,
        tools=tools,
        can_handoff_to=["ManagerAgent", "IdeaAnalysisAgent"],
    )

    # Idea Analysis Agent
    analysis_agent = FunctionAgent(
        name="IdeaAnalysisAgent",
        description="Evaluates and analyzes business ideas for viability and potential.",
        system_prompt=(
            f"{idea_analysis_agent_profile.backstory} "
            "After your analysis, hand off control back to the ManagerAgent."
        ),
        llm=llm,
        tools=tools,
        can_handoff_to=["ManagerAgent", "IdeationAgent"],
    )

    # Product Manager Agent
    product_manager_agent = FunctionAgent(
        name="ProductManagerAgent",
        description="Helps users understand and plan their app idea through a series of questions and generates PRD.",
        system_prompt=product_manager_agent_profile.backstory,
        llm=llm,
        tools=tools,
        can_handoff_to=["ManagerAgent"],
    )

    # Strategic Advisor Agent
    strategic_advisor_agent = FunctionAgent(
        name="StrategicAdvisorAgent",
        description="Provides strategic advice and actionable plans to help users achieve their goals.",
        system_prompt=strategic_advisor_agent_profile.backstory,
        llm=llm,
        tools=tools,
        can_handoff_to=["ManagerAgent"],
    )

    # Landing Page Designer Agent
    landing_page_designer_agent = FunctionAgent(
        name="LandingPageDesignerAgent",
        description="Guides beginners through planning and designing a landing page or personal portfolio.",
        system_prompt=landing_page_designer_agent_profile.backstory,
        llm=llm,
        tools=tools,
        can_handoff_to=["ManagerAgent"],
    )

    # CTO Agent
    cto_agent = FunctionAgent(
        name="CTOAgent",
        description="Helps developers understand and plan their app idea through a series of questions and generates a comprehensive masterplan.",
        system_prompt=cto_agent_profile.backstory,
        llm=llm,
        tools=tools,
        can_handoff_to=["ManagerAgent"],
    )

    # Advertising Strategist Agent
    advertising_strategist_agent = FunctionAgent(
        name="AdvertisingStrategistAgent",
        description="Analyzes and improves marketing copy using David Ogilvy's principles.",
        system_prompt=advertising_strategist_agent_profile.backstory,
        llm=llm,
        tools=tools,
        can_handoff_to=["ManagerAgent"],
    )

    return [
        manager_agent,
        ideation_agent,
        analysis_agent,
        product_manager_agent,
        strategic_advisor_agent,
        landing_page_designer_agent,
        cto_agent,
        advertising_strategist_agent,
    ]
