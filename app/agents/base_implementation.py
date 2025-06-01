"""Base implementation utilities for agents using LlamaIndex AgentWorkflow.

This module provides utility functions and patterns for creating
agents consistently across the application using LlamaIndex AgentWorkflow.
"""

from llama_index.core.agent.workflow import (
    FunctionAgent,
    AgentWorkflow,
    AgentOutput,
    ToolCallResult,
    ToolCall,
)
from app.core.types import AgentProfile
from app.llm import llm
from typing import Any, List, Optional
import asyncio


def create_function_agent(
    profile: AgentProfile,
    llm_instance: Any = None,
    tools: Optional[List] = None,
    can_handoff_to: Optional[List[str]] = None,
) -> FunctionAgent:
    """
    Create a LlamaIndex FunctionAgent with the given profile.

    This function provides a consistent way to create agents
    while reducing code duplication across agent modules.

    Args:
        profile: The agent profile containing role, goal, and backstory
        llm_instance: Optional LLM instance. If not provided, uses default llm
        tools: Optional list of tools for the agent
        can_handoff_to: Optional list of agent names this agent can hand off to

    Returns:
        Configured LlamaIndex FunctionAgent instance
    """
    if llm_instance is None:
        llm_instance = llm

    return FunctionAgent(
        name=profile.role.replace(" ", ""),  # Remove spaces for agent name
        description=profile.goal,
        system_prompt=profile.backstory,
        llm=llm_instance,
        tools=tools or [],
        can_handoff_to=can_handoff_to or [],
    )


class StreamingAgentWorkflow:
    """
    Wrapper class for AgentWorkflow that provides streaming execution.

    This class creates an AgentWorkflow and provides methods to run it
    with streaming events, following the LlamaIndex documentation pattern.
    """

    def __init__(self, profile: AgentProfile, llm_instance: Any = None):
        """
        Initialize the StreamingAgentWorkflow with a profile.

        Args:
            profile: The agent profile containing role, goal, and backstory
            llm_instance: Optional LLM instance. If not provided, uses default llm
        """
        self.profile = profile
        self.llm_instance = llm_instance or llm

        # Create a single FunctionAgent
        self.function_agent = create_function_agent(profile, llm_instance)

        # Create an AgentWorkflow with this single agent
        self.workflow = AgentWorkflow(
            agents=[self.function_agent],
            root_agent=self.function_agent.name,
            initial_state={},
        )

    async def run_streaming(self, input_data: str) -> str:
        """
        Execute the agent workflow with streaming events.

        Args:
            input_data: The input data for the agent to process

        Returns:
            The final agent response
        """
        handler = self.workflow.run(user_msg=input_data)

        current_agent = None
        final_response = ""

        async for event in handler.stream_events():
            if (
                hasattr(event, "current_agent_name")
                and event.current_agent_name != current_agent
            ):
                current_agent = event.current_agent_name
                print(f"\n{'='*50}")
                print(f"🤖 Agent: {current_agent}")
                print(f"{'='*50}\n")
            elif isinstance(event, AgentOutput):
                if event.response.content:
                    print("📤 Output:", event.response.content)
                    final_response = event.response.content
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
        return final_response or str(result)

    def _run_sync(self, input_data: str) -> str:
        """
        Helper method to run workflow synchronously.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.run_streaming(input_data))
            return result
        finally:
            loop.close()


def create_agent(
    profile: AgentProfile, llm_instance: Any = None
) -> StreamingAgentWorkflow:
    """
    Create a StreamingAgentWorkflow with the given profile.

    This function maintains backward compatibility with the existing
    create_agent interface while using LlamaIndex AgentWorkflow.

    Args:
        profile: The agent profile containing role, goal, and backstory
        llm_instance: Optional LLM instance. If not provided, uses default llm

    Returns:
        Configured StreamingAgentWorkflow instance
    """
    return StreamingAgentWorkflow(profile, llm_instance)


__all__ = ["create_agent", "create_function_agent", "StreamingAgentWorkflow"]
