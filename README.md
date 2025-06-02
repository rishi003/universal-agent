# Universal Agent

A modular and extensible agent system built with CrewAI for autonomous idea generation, analysis, and execution across various domains.

## Overview

The Universal Agent is a sophisticated system that leverages multiple specialized agents to generate, analyze, refine, and execute innovative ideas across different business domains. The application is built with a focus on clean architecture, maintainability, and extensibility, utilizing Chainlit for an interactive user interface.

## Architecture

### Core Components

- **Core Module** (`app/core/`): Foundational components including configuration, base classes, types, and factory patterns
- **Agents Module** (`app/agents/`): Specialized agents for different tasks and domains
- **LLM Module** (`app/llm/`): Language model configuration and utilities
- **Prompts Module** (`app/prompts/`): Agent-specific prompts and instructions
- **UI Module** (`public/`): Custom CSS and JavaScript for the Chainlit interface

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

### IdeaAnalysisAgent
- **Purpose**: Business idea evaluation and optimization
- **Specialization**: Market analysis, feasibility assessment, strategic recommendations

### ProductManagerAgent
- **Purpose**: Product development and management
- **Specialization**: Feature prioritization, roadmap planning, user story creation

### StrategicAdvisorAgent
- **Purpose**: High-level strategic planning and decision-making
- **Specialization**: Market trends analysis, competitive positioning, long-term strategy formulation

### LandingPageDesignerAgent
- **Purpose**: Design and optimization of landing pages
- **Specialization**: UI/UX design, conversion optimization, A/B testing strategies

### CTOAgent
- **Purpose**: Technical leadership and architecture planning
- **Specialization**: Technology stack selection, scalability planning, technical debt management

### AdvertisingStrategistAgent
- **Purpose**: Development and execution of advertising campaigns
- **Specialization**: Target audience analysis, ad copy creation, media planning

### ManagerAgent
- **Purpose**: Orchestration and coordination of other agents
- **Specialization**: Task delegation, progress monitoring, conflict resolution

## Project Structure

```
app/
├── core/                   # Core foundational components
├── agents/                 # Agent implementations
│   ├── ideation_agent/
│   ├── idea_analysis_agent/
│   ├── product_manager_agent/
│   ├── strategic_advisor_agent/
│   ├── landing_page_designer_agent/
│   ├── cto_agent/
│   ├── advertising_strategist_agent/
│   └── manager_agent/
├── llm/                    # Language model configuration
└── prompts/                # Agent prompts
public/                     # UI customization files
prisma-manager/             # Database management (if applicable)
```

## Configuration

The application uses environment variables for configuration. Key configurations are managed through `.chainlit/config.toml`.

## Key Features

1. **Modular Design**: Easy to extend with new agent types
2. **Type Safety**: Strong typing and runtime validation
3. **Error Handling**: Comprehensive error handling with logging
4. **Documentation**: Detailed docstrings and type hints
5. **Extensibility**: Factory and registry patterns for easy expansion
6. **Interactive UI**: Customized Chainlit interface for user interactions

## UI Customization

The Universal Agent uses Chainlit for its user interface, with custom styling and functionality:

- **Configuration**: Main UI settings in `.chainlit/config.toml`
- **Styling**: Custom styles in `public/custom.css`
- **Functionality**: Additional JavaScript in `public/custom.js`

## Usage

Refer to individual agent modules for specific usage instructions. The application is typically run using Chainlit:

```
chainlit run main.py
```

## Development Guidelines

### Adding New Agents

1. Create a new directory under `app/agents/`
2. Define the agent profile in `profile.py`
3. Implement the agent in `agent.py` using `create_agent()`
4. Add module documentation and exports in `__init__.py`
5. Update the main agents `__init__.py` to include the new agent

### Code Quality Standards

- Comprehensive docstrings
- Type hints for all functions
- Consistent error handling and logging
- Backward compatibility maintenance

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
