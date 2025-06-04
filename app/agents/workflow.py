"""Single unified workflow implementation using PydanticAI.

This module implements a unified agent system that handles all agents
and manages session-based agent switching with @ notation.
"""

from app.llm import model
from app.agents.base_implementation import create_pydantic_agent
from typing import Tuple, Optional
import re

# Import all agent profiles
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


class AgentWorkflow:
    """
    Unified agent workflow system using PydanticAI.

    This class manages all agents in a single workflow and handles
    session-based agent switching with @ notation parsing.
    """

    def __init__(self):
        """Initialize the unified agent workflow."""
        self.agents = self._create_all_agents()
        self.default_agent = "manager"

    def _create_all_agents(self) -> dict:
        """Create all PydanticAI agents."""
        return {
            "manager": create_pydantic_agent(manager_agent_profile, model),
            "ideation": create_pydantic_agent(ideation_agent_profile, model),
            "ideaanalysis": create_pydantic_agent(idea_analysis_agent_profile, model),
            "productmanager": create_pydantic_agent(
                product_manager_agent_profile, model
            ),
            "strategicadvisor": create_pydantic_agent(
                strategic_advisor_agent_profile, model
            ),
            "landingpage": create_pydantic_agent(
                landing_page_designer_agent_profile, model
            ),
            "cto": create_pydantic_agent(cto_agent_profile, model),
            "advertisingstrategist": create_pydantic_agent(
                advertising_strategist_agent_profile, model
            ),
        }

    def parse_agent_switch(self, message: str) -> Tuple[Optional[str], str]:
        """
        Parse @ notation from message.

        Args:
            message: The user message that may contain @ notation

        Returns:
            Tuple of (agent_name, cleaned_message)
            agent_name is None if no valid @ notation found
        """
        message = message.strip()

        if not message.startswith("@"):
            return None, message

        # Split on first space to get @agent and remainder
        parts = message.split(" ", 1)
        agent_part = parts[0][1:].lower()  # Remove @ and lowercase
        remainder = parts[1] if len(parts) > 1 else ""

        # Check if it's a valid agent
        if agent_part in self.agents:
            return agent_part, remainder.strip()

        # Invalid agent, return original message
        return None, message

    def get_agent(self, agent_name: str):
        """
        Get agent by name, fallback to default agent.

        Args:
            agent_name: Name of the agent to retrieve

        Returns:
            PydanticAI Agent instance
        """
        return self.agents.get(agent_name, self.agents[self.default_agent])

    def get_agent_profile_name(self, agent_name: str) -> str:
        """Get human-readable agent name for display."""
        profile_map = {
            "manager": "Manager Agent",
            "ideation": "Ideation Agent",
            "ideaanalysis": "Idea Analysis Agent",
            "productmanager": "Product Manager Agent",
            "strategicadvisor": "Strategic Advisor Agent",
            "landingpage": "Landing Page Designer Agent",
            "cto": "CTO Agent",
            "advertisingstrategist": "Advertising Strategist Agent",
        }
        return profile_map.get(agent_name, "Unknown Agent")

    async def run_streaming(
        self, message: str, current_agent: str, message_history: list = None
    ) -> Tuple[str, str]:
        """
        Execute the workflow with streaming events.

        Args:
            message: The user's message
            current_agent: Currently active agent name
            message_history: List of PydanticAI ModelMessage objects for conversation history

        Returns:
            Tuple of (response, new_current_agent)
        """
        # Parse for agent switching
        switch_agent, cleaned_message = self.parse_agent_switch(message)

        # Determine which agent to use
        if switch_agent:
            # User is switching agents
            target_agent_name = switch_agent
            user_input = cleaned_message
            print(f"\n🔄 Switching to {self.get_agent_profile_name(target_agent_name)}")
        else:
            # Continue with current agent
            target_agent_name = current_agent
            user_input = message

        # Get the target agent
        agent = self.get_agent(target_agent_name)

        # Display agent info
        print(f"\n{'='*50}")
        print(f"🤖 Active Agent: {self.get_agent_profile_name(target_agent_name)}")
        print(f"{'='*50}\n")

        # Use message_history directly (already in PydanticAI format)
        if message_history is None:
            message_history = []

        try:
            # Execute with PydanticAI streaming
            async with agent.run_stream(
                user_input, message_history=message_history
            ) as result:
                full_response = ""
                async for text in result.stream_text():
                    print(text, end="", flush=True)
                    full_response = text

                print(
                    f"\n\n✅ {self.get_agent_profile_name(target_agent_name)} completed!"
                )
                print("=" * 60)

                return full_response, target_agent_name

        except Exception as e:
            error_msg = (
                f"Error in {self.get_agent_profile_name(target_agent_name)}: {str(e)}"
            )
            print(f"❌ {error_msg}")
            return error_msg, target_agent_name

    def list_agents(self) -> list[str]:
        """Get list of all available agent names."""
        return list(self.agents.keys())

    def list_agent_display_names(self) -> list[str]:
        """Get list of all available agent display names."""
        return [self.get_agent_profile_name(name) for name in self.agents.keys()]


# Global workflow instance
agent_workflow = AgentWorkflow()


__all__ = ["AgentWorkflow", "agent_workflow"]
