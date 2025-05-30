# Universal Agent

A modular and extensible agent system built with CrewAI for autonomous idea generation and analysis.

## Overview

The Universal Agent is a sophisticated system that leverages multiple specialized agents to generate, analyze, and refine innovative ideas. The application is built with a focus on clean architecture, maintainability, and extensibility.

## Architecture

### Core Components

- **Core Module** (`app/core/`): Foundational components including configuration, base classes, types, and factory patterns
- **Agents Module** (`app/agents/`): Specialized agents for different tasks
- **LLM Module** (`app/llm/`): Language model configuration and utilities
- **Prompts Module** (`app/prompts/`): Agent-specific prompts and instructions

### Design Patterns

1. **Factory Pattern**: Consistent agent creation through `create_agent()` utility
2. **Base Classes**: Abstract base classes for common functionality
3. **Type Safety**: Pydantic models for configuration and data validation
4. **Registry Pattern**: Centralized agent and profile management
5. **Modular Architecture**: Clear separation of concerns across modules

## Available Agents

### IdeationAgent
- **Purpose**: Autonomous idea generation and recursive refinement
- **Specialization**: Creative thinking, iterative improvement, comprehensive ideation
- **Process**: Minimum 25 iterations of self-directed analysis and refinement

### IdeaAnalysisAgent
- **Purpose**: Business idea evaluation and optimization
- **Specialization**: Market analysis, feasibility assessment, strategic recommendations
- **Output**: Structured analysis with viability rankings and actionable insights

## Project Structure

```
app/
├── core/                   # Core foundational components
│   ├── __init__.py        # Module exports
│   ├── base.py            # Base classes and registry
│   ├── config.py          # Application configuration
│   ├── factory.py         # Factory patterns
│   └── types.py           # Type definitions
├── agents/                # Agent implementations
│   ├── __init__.py        # Agent exports
│   ├── base_implementation.py  # Agent utilities
│   ├── ideation_agent/    # Ideation agent module
│   │   ├── __init__.py
│   │   ├── agent.py       # Agent implementation
│   │   └── profile.py     # Agent profile
│   └── idea_analysis_agent/  # Analysis agent module
│       ├── __init__.py
│       ├── agent.py       # Agent implementation
│       └── profile.py     # Agent profile
├── llm/                   # Language model configuration
│   ├── __init__.py
│   └── llm.py            # LLM setup and utilities
└── prompts/              # Agent prompts
    ├── __init__.py
    ├── ideation_agent_prompt.py
    └── idea_analysis_agent_prompt.py
```

## Configuration

The application uses environment variables for configuration:

- `OPENROUTER_API_KEY`: API key for OpenRouter service
- `OPENROUTER_BASE_URL`: Base URL for OpenRouter API (default: https://api.openrouter.ai/v1)

## Key Features

### 1. Modular Design
- Clean separation between agents, core functionality, and configuration
- Easy to extend with new agent types
- Consistent patterns across all modules

### 2. Type Safety
- Pydantic models for all configuration and data structures
- Strong typing throughout the codebase
- Runtime validation of inputs and outputs

### 3. Error Handling
- Comprehensive error handling with logging
- Graceful degradation for user-facing errors
- Detailed logging for debugging and monitoring

### 4. Documentation
- Comprehensive docstrings for all modules, classes, and functions
- Clear module-level documentation
- Type hints for better IDE support

### 5. Extensibility
- Factory pattern for easy agent creation
- Registry pattern for agent management
- Base classes for consistent agent behavior

## Usage

### Basic Usage
```python
from app.agents import IdeationAgent

# Use the agent directly
response = IdeationAgent.kickoff("Create an AI sales assistant")
```

### Creating Custom Agents
```python
from app.agents import create_agent
from app.core.types import AgentProfile

# Define a custom profile
custom_profile = AgentProfile(
    role="Custom Agent",
    goal="Perform custom tasks",
    backstory="Specialized agent for custom functionality"
)

# Create the agent
custom_agent = create_agent(custom_profile)
```

## Development Guidelines

### Adding New Agents

1. Create a new directory under `app/agents/`
2. Define the agent profile in `profile.py`
3. Implement the agent in `agent.py` using `create_agent()`
4. Add module documentation and exports in `__init__.py`
5. Update the main agents `__init__.py` to include the new agent

### Code Quality Standards

- All modules must have comprehensive docstrings
- Use type hints for all function parameters and return values
- Follow the established patterns for consistency
- Include error handling and logging where appropriate
- Maintain backward compatibility when making changes

## Dependencies

- **CrewAI**: Core agent framework
- **Chainlit**: Web interface for user interactions
- **Pydantic**: Data validation and settings management
- **Python-dotenv**: Environment variable management

## Running the Application

1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables in `.env` file
3. Run the application: `chainlit run main.py`

## Contributing

When contributing to this project:

1. Follow the established architectural patterns
2. Maintain comprehensive documentation
3. Include appropriate error handling
4. Add type hints and validation
5. Test your changes thoroughly
6. Respect existing parameters and interfaces

The codebase is designed for maintainability and extensibility. Please ensure any changes align with these principles.
