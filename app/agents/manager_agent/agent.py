"""Manager Agent implementation.

This module contains the ManagerAgent that oversees activities,
maintains plans, coordinates between agents, and provides conversational guidance.
"""

from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.workflow import Context
from app.llm import llm
from .profile import manager_agent_profile
from typing import Dict, List, Any, Optional
import json
from datetime import datetime


# Manager Agent Tools
async def create_plan(ctx: Context, user_request: str, plan_details: str) -> str:
    """Tool for creating and storing a comprehensive plan for the user's request."""
    current_state = await ctx.get("state")

    plan = {
        "user_request": user_request,
        "plan_details": plan_details,
        "created_at": datetime.now().isoformat(),
        "status": "created",
        "steps": [],
        "current_step": 0,
        "agent_assignments": {},
        "results": {},
    }

    current_state["plan"] = plan
    await ctx.set("state", current_state)

    return f"Plan created successfully. Plan details: {plan_details}"


async def update_plan(ctx: Context, updates: str, status: str = None) -> str:
    """Tool for updating the current plan with new information or status changes."""
    current_state = await ctx.get("state")

    if "plan" not in current_state:
        return "No plan exists to update. Please create a plan first."

    plan = current_state["plan"]
    plan["plan_details"] += f"\n\nUpdate ({datetime.now().isoformat()}): {updates}"

    if status:
        plan["status"] = status

    current_state["plan"] = plan
    await ctx.set("state", current_state)

    return f"Plan updated successfully. Status: {plan['status']}"


async def add_plan_step(
    ctx: Context, step_description: str, assigned_agent: str = None
) -> str:
    """Tool for adding a new step to the current plan."""
    current_state = await ctx.get("state")

    if "plan" not in current_state:
        return "No plan exists. Please create a plan first."

    plan = current_state["plan"]
    step = {
        "description": step_description,
        "assigned_agent": assigned_agent,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "result": None,
    }

    plan["steps"].append(step)

    if assigned_agent:
        if "agent_assignments" not in plan:
            plan["agent_assignments"] = {}
        plan["agent_assignments"][assigned_agent] = len(plan["steps"]) - 1

    current_state["plan"] = plan
    await ctx.set("state", current_state)

    return f"Step added to plan: {step_description}" + (
        f" (assigned to {assigned_agent})" if assigned_agent else ""
    )


async def get_plan_status(ctx: Context) -> str:
    """Tool for retrieving the current plan status and progress."""
    current_state = await ctx.get("state")

    if "plan" not in current_state:
        return "No plan exists yet."

    plan = current_state["plan"]

    status_report = f"""
Current Plan Status:
- Request: {plan['user_request']}
- Status: {plan['status']}
- Created: {plan['created_at']}
- Total Steps: {len(plan['steps'])}
- Current Step: {plan['current_step']}

Plan Details:
{plan['plan_details']}

Steps:
"""

    for i, step in enumerate(plan["steps"]):
        status_indicator = (
            "✅"
            if step["status"] == "completed"
            else "🔄" if step["status"] == "in_progress" else "⏳"
        )
        agent_info = (
            f" (assigned to {step['assigned_agent']})" if step["assigned_agent"] else ""
        )
        status_report += (
            f"{i+1}. {status_indicator} {step['description']}{agent_info}\n"
        )

    return status_report


async def assign_task_to_agent(
    ctx: Context, agent_name: str, task_description: str, step_index: int = None
) -> str:
    """Tool for assigning a specific task to an agent and tracking the assignment."""
    current_state = await ctx.get("state")

    if "plan" not in current_state:
        return "No plan exists. Please create a plan first."

    plan = current_state["plan"]

    # Create assignment record
    assignment = {
        "agent_name": agent_name,
        "task_description": task_description,
        "assigned_at": datetime.now().isoformat(),
        "status": "assigned",
        "step_index": step_index,
    }

    if "agent_assignments" not in plan:
        plan["agent_assignments"] = {}

    plan["agent_assignments"][agent_name] = assignment

    # Update step if step_index is provided
    if step_index is not None and step_index < len(plan["steps"]):
        plan["steps"][step_index]["assigned_agent"] = agent_name
        plan["steps"][step_index]["status"] = "assigned"

    current_state["plan"] = plan
    await ctx.set("state", current_state)

    return f"Task assigned to {agent_name}: {task_description}"


async def record_agent_result(
    ctx: Context, agent_name: str, result: str, step_index: int = None
) -> str:
    """Tool for recording results from agent execution."""
    current_state = await ctx.get("state")

    if "plan" not in current_state:
        current_state["plan"] = {"results": {}}

    plan = current_state["plan"]

    if "results" not in plan:
        plan["results"] = {}

    plan["results"][agent_name] = {
        "result": result,
        "completed_at": datetime.now().isoformat(),
        "step_index": step_index,
    }

    # Update step status if step_index is provided
    if step_index is not None and "steps" in plan and step_index < len(plan["steps"]):
        plan["steps"][step_index]["status"] = "completed"
        plan["steps"][step_index]["result"] = result

    current_state["plan"] = plan
    await ctx.set("state", current_state)

    return (
        f"Result recorded for {agent_name}: {result[:100]}..."
        if len(result) > 100
        else f"Result recorded for {agent_name}: {result}"
    )


async def get_available_agents(ctx: Context) -> str:
    """Tool for getting information about available agents and their capabilities."""
    agents_info = """
Available Agents and Their Capabilities:

1. **IdeationAgent**
   - Role: Generates innovative ideas using recursive thinking and creative processes
   - Best for: Brainstorming, creative problem solving, generating multiple solution options
   - Can hand off to: IdeaAnalysisAgent

2. **IdeaAnalysisAgent** 
   - Role: Evaluates and analyzes business ideas for viability and potential
   - Best for: Feasibility analysis, risk assessment, business evaluation, market analysis
   - Can hand off to: IdeationAgent

3. **ManagerAgent** (You)
   - Role: Oversees activities, maintains plans, coordinates between agents
   - Best for: Project coordination, planning, user guidance, workflow management
   - Can hand off to: Any agent based on task requirements

Agent Selection Guidelines:
- For creative tasks requiring new ideas: Use IdeationAgent
- For analysis and evaluation tasks: Use IdeaAnalysisAgent  
- For complex tasks requiring multiple steps: Use ManagerAgent to coordinate
- For tasks requiring both ideation and analysis: Start with IdeationAgent, then hand off to IdeaAnalysisAgent
"""

    return agents_info


# Create the ManagerAgent
def create_manager_agent() -> FunctionAgent:
    """Create the ManagerAgent with all necessary tools and capabilities."""

    tools = [
        create_plan,
        update_plan,
        add_plan_step,
        get_plan_status,
        assign_task_to_agent,
        record_agent_result,
        get_available_agents,
    ]

    return FunctionAgent(
        name="ManagerAgent",
        description="Oversees activities, maintains comprehensive plans, coordinates between agents, and provides conversational guidance to users",
        system_prompt=manager_agent_profile.backstory,
        llm=llm,
        tools=tools,
        can_handoff_to=["IdeationAgent", "IdeaAnalysisAgent"],
    )


# Create the agent instance
ManagerAgent = create_manager_agent()

__all__ = ["ManagerAgent", "create_manager_agent"]
