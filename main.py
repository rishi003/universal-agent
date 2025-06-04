"""Main application entry point for the Universal Agent.

This module sets up the Chainlit interface and handles user interactions
with the unified agent workflow using PydanticAI.
"""

import chainlit as cl
from chainlit.types import ThreadDict
from dotenv import load_dotenv
from typing import Dict, Optional, List
import logging
from app.agents import agent_workflow
from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, TextPart

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


@cl.set_starters
async def set_starters():
    """Set starter suggestions for users to quickly begin conversations."""
    return [
        cl.Starter(
            label="💡 Generate Startup Ideas",
            message="@ideation Give me 5 innovative startup ideas for sustainable technology that could solve real-world problems",
        ),
        cl.Starter(
            label="📊 Analyze Business Idea",
            message="@analysis I have an idea for a meal planning app that uses AI to suggest recipes based on dietary restrictions and available ingredients. Can you evaluate its market potential?",
        ),
        cl.Starter(
            label="🏗️ Plan Technical Architecture",
            message="@cto I need to build a mobile app that handles real-time chat, user profiles, and file sharing. What technology stack would you recommend for scalability?",
        ),
        cl.Starter(
            label="📋 Create Product Roadmap",
            message="@product Help me create a 6-month product roadmap for a fitness tracking app with social features. What should be the priority features?",
        ),
        cl.Starter(
            label="🎯 Develop Marketing Strategy",
            message="@advertising I'm launching a B2B SaaS tool for project management. Create a comprehensive marketing strategy to reach small to medium businesses",
        ),
        cl.Starter(
            label="🎨 Design Landing Page",
            message="@landing I need a high-converting landing page for an AI writing assistant. What elements should I include and how should I structure it?",
        ),
        cl.Starter(
            label="📈 Strategic Business Planning",
            message="@strategic I want to enter the e-commerce market with handmade crafts. Help me develop a competitive strategy and positioning plan",
        ),
        cl.Starter(
            label="🔄 Coordinate Complex Project",
            message="@manager I'm building a fintech startup with mobile app, web dashboard, and API. Help me create a comprehensive project plan and coordinate the development phases",
        ),
    ]


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
    # Initialize empty message history for PydanticAI
    message_history: List[ModelMessage] = []
    cl.user_session.set("message_history", message_history)
    cl.user_session.set("current_agent", "manager")  # Default to manager


@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming messages from users."""
    await process_message(message)


@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    """Handle resuming a chat session."""
    logger.info(f"Resuming chat session for thread")

    # Initialize message history for PydanticAI
    message_history: List[ModelMessage] = []
    root_messages = [m for m in thread["steps"] if m["parentId"] == None]

    for message in root_messages:
        if message["type"] == "user_message":
            # Add user message to history
            message_history.append(ModelRequest.user_text_prompt(message["output"]))
        else:
            # Add assistant message to history
            message_history.append(
                ModelResponse(parts=[TextPart(content=message["output"])])
            )

    cl.user_session.set("message_history", message_history)
    cl.user_session.set("current_agent", "manager")  # Reset to manager on resume


async def process_message(message: cl.Message):
    """Process incoming messages and generate responses."""
    try:
        logger.info(f"Processing message: {message.content[:100]}...")

        # Create a message to show processing has started
        processing_msg = cl.Message(content="🤖 Processing your request...")
        await processing_msg.send()

        # Get message history and current agent from session
        message_history = cl.user_session.get("message_history", [])
        current_agent = cl.user_session.get("current_agent", "manager")

        # Add current user message to history
        message_history.append(ModelRequest.user_text_prompt(message.content))

        # Use the unified workflow to process the message
        response, new_agent = await agent_workflow.run_streaming(
            message.content, current_agent, message_history
        )

        # Update the current agent in session if it changed
        cl.user_session.set("current_agent", new_agent)

        # Add response to message history
        message_history.append(ModelResponse(parts=[TextPart(content=response)]))
        cl.user_session.set("message_history", message_history)

        # Update the processing message with the final response
        processing_msg.content = response
        await processing_msg.update()

        logger.info("Message processed successfully")

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        error_message = "I apologize, but I encountered an error while processing your request. Please try again."
        await cl.Message(content=error_message).send()
