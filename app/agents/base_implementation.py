"""Base implementation utilities for agents using PydanticAI.

This module provides utility functions and patterns for creating
agents consistently across the application using PydanticAI.
"""

from pydantic_ai import Agent
from app.core.types import AgentProfile
from app.llm import model
from typing import Any, Optional
import asyncio


def create_pydantic_agent(
    profile: AgentProfile,
    model_instance: Any = None,
) -> Agent:
    """
    Create a PydanticAI Agent with the given profile.

    This function provides a consistent way to create agents
    while reducing code duplication across agent modules.

    Args:
        profile: The agent profile containing role, goal, and backstory
        model_instance: Optional model instance. If not provided, uses default model

    Returns:
        Configured PydanticAI Agent instance
    """
    if model_instance is None:
        model_instance = model

    return Agent(
        model_instance,
        system_prompt=profile.backstory,
    )


class StreamingAgentWrapper:
    """
    Wrapper class for PydanticAI Agent that provides consistent streaming execution.

    This class wraps a PydanticAI Agent and provides methods to run it
    with streaming events, maintaining compatibility with the existing interface.
    """

    def __init__(self, profile: AgentProfile, model_instance: Any = None):
        """
        Initialize the StreamingAgentWrapper with a profile.

        Args:
            profile: The agent profile containing role, goal, and backstory
            model_instance: Optional model instance. If not provided, uses default model
        """
        self.profile = profile
        self.model_instance = model_instance or model
        self.agent = create_pydantic_agent(profile, model_instance)

    async def run_streaming(self, input_data: str, message_history: list = None) -> str:
        """
        Execute the agent with streaming events.

        Args:
            input_data: The input data for the agent to process
            message_history: List of PydanticAI ModelMessage objects for conversation history

        Returns:
            The final agent response
        """
        print(f"\n{'='*50}")
        print(f"🤖 Agent: {self.profile.role}")
        print(f"{'='*50}\n")

        # Use message_history directly (already in PydanticAI format)
        if message_history is None:
            message_history = []

        try:
            # Use PydanticAI streaming
            async with self.agent.run_stream(
                input_data, message_history=message_history
            ) as result:
                full_response = ""
                async for text in result.stream_text():
                    print(text, end="", flush=True)
                    full_response = (
                        text  # stream_text() provides complete text each time
                    )

                print("\n")  # New line after streaming
                print(f"✅ {self.profile.role} completed!")
                print("=" * 60)

                return full_response

        except Exception as e:
            error_msg = f"Error in {self.profile.role}: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg

    def _run_sync(self, input_data: str, message_history: list = None) -> str:
        """
        Helper method to run agent synchronously.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                self.run_streaming(input_data, message_history)
            )
            return result
        finally:
            loop.close()


def create_agent(
    profile: AgentProfile, model_instance: Any = None
) -> StreamingAgentWrapper:
    """
    Create a StreamingAgentWrapper with the given profile.

    This function maintains backward compatibility with the existing
    create_agent interface while using PydanticAI under the hood.

    Args:
        profile: The agent profile containing role, goal, and backstory
        model_instance: Optional model instance. If not provided, uses default model

    Returns:
        Configured StreamingAgentWrapper instance
    """
    return StreamingAgentWrapper(profile, model_instance)


__all__ = ["create_agent", "create_pydantic_agent", "StreamingAgentWrapper"]
