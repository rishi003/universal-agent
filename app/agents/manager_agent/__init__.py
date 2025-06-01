"""Manager Agent module.

This module contains the ManagerAgent that oversees activities,
maintains plans, and coordinates between different agents.
"""

from .agent import ManagerAgent
from .profile import manager_agent_profile

__all__ = ["ManagerAgent", "manager_agent_profile"]
