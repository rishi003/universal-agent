"""Multi-agent workflow implementation using LlamaIndex AgentWorkflow.

This module implements a dynamic multi-agent system that can handle
multiple agents collaborating to complete tasks.
"""

from llama_index.core.agent.workflow import (
    FunctionAgent,
    AgentWorkflow,
    AgentOutput,
    ToolCallResult,
    ToolCall,
)
from llama_index.core.workflow import Context
from llama_index.core.memory import Memory
from llama_index.core.llms import ChatMessage, MessageRole
from app.llm import llm
from app.agents.ideation_agent.profile import ideation_agent_profile
from app.agents.idea_analysis_agent.profile import idea_analysis_agent_profile
from app.agents.manager_agent.profile import manager_agent_profile
from typing import Dict, List, Any
import asyncio


# State management tools
async def save_ideas(ctx: Context, ideas: str, ideas_title: str) -> str:
    """Tool for saving generated ideas to the workflow state."""
    current_state = await ctx.get("state")
    if "generated_ideas" not in current_state:
        current_state["generated_ideas"] = {}
    current_state["generated_ideas"][ideas_title] = ideas
    await ctx.set("state", current_state)
    return "Ideas saved successfully."


async def save_analysis(ctx: Context, analysis: str) -> str:
    """Tool for saving idea analysis to the workflow state."""
    current_state = await ctx.get("state")
    current_state["analysis_result"] = analysis
    await ctx.set("state", current_state)
    return "Analysis saved successfully."


class UniversalAgentWorkflow:
    """
    Dynamic multi-agent workflow system.

    This class creates and manages a multi-agent workflow that can be
    easily extended with new agents.
    """

    def __init__(self):
        """Initialize the multi-agent workflow."""
        self.agents = self._create_agents()
        self.workflow = self._create_workflow()

    def _create_agents(self) -> List[FunctionAgent]:
        """Create all agents for the workflow including the ManagerAgent."""
        # Manager Agent
        manager_agent = FunctionAgent(
            name="ManagerAgent",
            description="Oversees activities, maintains plans, and coordinates between agents.",
            system_prompt=manager_agent_profile.backstory,
            llm=llm,
            tools=[save_ideas, save_analysis],
            can_handoff_to=["IdeationAgent", "IdeaAnalysisAgent"],
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
            tools=[save_ideas],
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
            tools=[save_analysis],
            can_handoff_to=["ManagerAgent", "IdeationAgent"],
        )

        return [manager_agent, ideation_agent, analysis_agent]

    def _create_workflow(self) -> AgentWorkflow:
        """Create the AgentWorkflow with ManagerAgent as the root."""
        return AgentWorkflow(
            agents=self.agents,
            root_agent="ManagerAgent",  # Start with the manager
            initial_state={
                "plan": "No plan yet.",
                "generated_ideas": {},
                "analysis_result": "Not analyzed yet.",
                "user_request": "",
            },
        )

    async def run_streaming(self, user_msg: str, memory: Memory = None) -> str:
        """
        Run the multi-agent workflow with streaming events.

        Args:
            user_msg: The user's request
            chat_history: List of previous chat messages

        Returns:
            The final result from the workflow
        """

        # Update initial state with user request and chat history
        handler = self.workflow.run(user_msg=user_msg, memory=memory)

        current_agent = None
        final_response = ""

        print(f"\n🚀 Starting Multi-Agent Workflow")
        print(f"📝 User Request: {user_msg}")
        print("=" * 60)

        async for event in handler.stream_events():
            if (
                hasattr(event, "current_agent_name")
                and event.current_agent_name != current_agent
            ):
                current_agent = event.current_agent_name
                print(f"\n{'='*50}")
                print(f"🤖 Agent: {current_agent}")
                print(f"{'='*50}")
            elif isinstance(event, AgentOutput):
                if event.response.content:
                    print(f"📤 Output: {event.response.content}")
                    final_response = event.response.content
                    # Add agent response to memory
                    memory.put(
                        ChatMessage(role=MessageRole.ASSISTANT, content=final_response)
                    )
                if event.tool_calls:
                    print(
                        "🛠️  Planning to use tools:",
                        [call.tool_name for call in event.tool_calls],
                    )
            elif isinstance(event, ToolCallResult):
                print(f"🔧 Tool Result ({event.tool_name}):")
                print(f"  Arguments: {event.tool_kwargs}")
                print(f"  Output: {event.tool_output}")
            elif isinstance(event, ToolCall):
                print(f"🔨 Calling Tool: {event.tool_name}")
                print(f"  With arguments: {event.tool_kwargs}")

        # Get the final result
        result = await handler
        print(f"\n✅ Workflow completed!")
        print("=" * 60)

        return final_response or str(result)

    def add_agent(self, agent: FunctionAgent) -> None:
        """
        Add a new agent to the workflow dynamically.

        Args:
            agent: The FunctionAgent to add
        """
        self.agents.append(agent)
        # Recreate workflow with new agent
        self.workflow = AgentWorkflow(
            agents=self.agents,
            root_agent=self.workflow.root_agent,
            initial_state=self.workflow.initial_state,
        )
        print(f"✅ Added agent: {agent.name}")

    def list_agents(self) -> List[str]:
        """Get list of all agent names in the workflow."""
        return [agent.name for agent in self.agents]


# Global workflow instance
universal_workflow = UniversalAgentWorkflow()


__all__ = [
    "UniversalAgentWorkflow",
    "universal_workflow",
]
