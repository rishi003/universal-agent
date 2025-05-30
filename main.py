"""Main application entry point for the Universal Agent.

This module sets up the Chainlit interface and handles user interactions
with the various agents available in the system.
"""

import chainlit as cl
from dotenv import load_dotenv
from typing import Dict, Optional
import logging
from app.agents import IdeationAgent, IdeaAnalysisAgent


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


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages from users.

    This function processes user messages and routes them to the
    appropriate agent for processing.

    Args:
        message: The incoming message from the user
    """
    try:
        logger.info(f"Processing message: {message.content[:100]}...")

        # Use the IdeationAgent to process the message
        response = IdeationAgent.kickoff(message.content)

        # Send the response back to the user
        await cl.Message(content=response.raw).send()

        logger.info("Message processed successfully")

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        error_message = "I apologize, but I encountered an error while processing your request. Please try again."
        await cl.Message(content=error_message).send()
