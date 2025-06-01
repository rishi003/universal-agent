"""Agent module initialization.

This module exports the main agents used in the application.
The agents are now implemented using LlamaIndex AgentWorkflow
for multi-agent collaboration.
"""

from .workflow import (
    universal_workflow,
    UniversalAgentWorkflow,
)

__all__ = [
    "universal_workflow",
    "UniversalAgentWorkflow",
]
