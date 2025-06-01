"""Main application entry point for the Universal Agent.

This module sets up the Chainlit interface and handles user interactions
with the various agents available in the system.
"""

import chainlit as cl
from chainlit.types import ThreadDict
from dotenv import load_dotenv
from typing import Dict, Optional
import logging
from app.agents import universal_workflow
from llama_index.core.memory import Memory
from llama_index.core.llms import ChatMessage, MessageRole

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],
    default_user: cl.User,
) -> Optional[cl.User]:
    """Handle OAuth authentication callback.

    Args:
        provider_id: The OAuth provider identifier
        token: The authentication token
        raw_user_data: Raw user data from the provider
        default_user: Default user object

    Returns:
        User object for the authenticated user
    """
    logger.info(f"OAuth callback for provider: {provider_id}")
    return default_user


@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session."""
    logger.info("Starting new chat session")
    memory = Memory.from_defaults(session_id="chainlit_session", token_limit=40000)
    cl.user_session.set("memory", memory)


@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming messages from users."""
    await process_message(message)


@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    """Handle resuming a chat session."""
    logger.info(f"Resuming chat session for thread")

    memory = Memory.from_defaults(session_id=thread.get("id"), token_limit=40000)
    root_messages = [m for m in thread["steps"] if m["parentId"] == None]

    for message in root_messages:
        if message["type"] == "user_message":
            memory.put(ChatMessage(role=MessageRole.USER, content=message["output"]))
        else:
            memory.put(
                ChatMessage(role=MessageRole.ASSISTANT, content=message["output"])
            )

    cl.user_session.set("memory", memory)

    await cl.Message(
        content="Welcome back! Resuming your previous conversation."
    ).send()


async def process_message(message: cl.Message):
    """Process incoming messages and generate responses."""
    try:
        logger.info(f"Processing message: {message.content[:100]}...")

        # Create a message to show processing has started
        processing_msg = cl.Message(content="🤖 Processing your request...")
        await processing_msg.send()

        # Get memory
        memory = cl.user_session.get("memory")

        # Add current message to memory
        memory.put(ChatMessage(role=MessageRole.USER, content=message.content))

        # Use the ManagerAgent to process the message with streaming
        response = await universal_workflow.run_streaming(message.content, memory)

        # Add response to memory
        memory.put(ChatMessage(role=MessageRole.ASSISTANT, content=response))

        # Update the processing message with the final response
        processing_msg.content = response
        await processing_msg.update()

        logger.info("Message processed successfully")

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        error_message = "I apologize, but I encountered an error while processing your request. Please try again."
        await cl.Message(content=error_message).send()
