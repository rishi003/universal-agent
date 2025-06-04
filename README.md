# Universal Agent 🚀🤖

A modern AI-powered agent system built with PydanticAI for autonomous idea generation, analysis, and execution across various business domains.

## Overview

The Universal Agent is a sophisticated system that leverages multiple specialized AI agents to generate, analyze, refine, and execute innovative ideas across different business domains. The application has been modernized with PydanticAI and features a unified workflow system with seamless agent switching capabilities via an interactive Chainlit interface.

## 🎯 Key Features

- **8 Specialized AI Agents**: Each with unique personalities and capabilities
- **@ Notation System**: Switch between agents using `@agent_name` 
- **Session Persistence**: Agents remain active until explicitly switched
- **Streaming Responses**: Real-time AI responses with PydanticAI
- **Modern Architecture**: Built with PydanticAI, OpenRouter, and Chainlit
- **Unified Workflow**: Single workflow system managing all agents

## 🤖 Available Agents

| Agent | Command | Specialization |
|-------|---------|----------------|
| **Manager Agent** | `@manager` | Orchestration, planning, task coordination |
| **Ideation Agent** | `@ideation` | Creative thinking, idea generation, innovation |
| **Idea Analysis Agent** | `@analysis` | Market evaluation, feasibility assessment |
| **Product Manager Agent** | `@product` | Feature prioritization, roadmap planning |
| **Strategic Advisor Agent** | `@strategic` | High-level strategy, market positioning |
| **Landing Page Designer** | `@landing` | UI/UX design, conversion optimization |
| **CTO Agent** | `@cto` | Technical architecture, scalability planning |
| **Advertising Strategist** | `@advertising` | Campaign development, ad strategy |

## 🏗️ Architecture

### Core Components

- **Unified Workflow System** (`app/agents/workflow.py`): Single AgentWorkflow class managing all agents
- **PydanticAI Integration** (`app/llm/`): Modern AI framework with OpenRouter support
- **Agent Profiles** (`app/agents/*/profile.py`): Agent personalities and capabilities
- **Base Implementation** (`app/agents/base_implementation.py`): Shared agent functionality
- **Session Management**: Persistent agent switching with memory

### Design Patterns

1. **Unified Workflow**: Single workflow system handling all agent interactions
2. **Agent Switching**: Parse `@agent_name` notation for seamless transitions
3. **Session Persistence**: Remember active agent across conversation
4. **Streaming Responses**: Real-time token streaming with PydanticAI
5. **Memory Integration**: LlamaIndex memory for conversation history

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- OpenRouter API Key
- UV package manager (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd universal-agent
   ```

2. **Install dependencies**
   ```bash
   uv sync
   # or
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenRouter API key
   ```

4. **Run the application**
   ```bash
   chainlit run main.py
   # or specify port
   chainlit run main.py --port 8000
   ```

## 💬 Usage Examples

### Basic Conversation
```
User: "Help me brainstorm app ideas"
→ Manager Agent (default)

User: "@ideation give me 5 startup ideas for AI tools"
→ Switches to Ideation Agent

User: "Can you expand on the first idea?"
→ Still uses Ideation Agent (session persistence)

User: "@cto how would I build this technically?"
→ Switches to CTO Agent
```

### Agent Switching Commands
- `@manager` - Coordinate and plan complex projects
- `@ideation` - Generate creative ideas and innovations
- `@analysis` - Evaluate business ideas and market fit
- `@product` - Plan product features and roadmaps
- `@strategic` - Develop high-level business strategy
- `@landing` - Design landing pages and optimize conversion
- `@cto` - Plan technical architecture and implementation
- `@advertising` - Create marketing campaigns and ad strategies

## 🔧 Technical Implementation

### PydanticAI Migration

The system has been migrated from LlamaIndex to PydanticAI for improved performance and modern AI capabilities:

- **Before**: Multiple LlamaIndex FunctionAgents with separate workflows
- **After**: Single PydanticAI AgentWorkflow with unified agent management
- **Benefits**: Cleaner code, better streaming, improved session management

### Key Files

```
app/
├── agents/
│   ├── workflow.py              # Unified workflow system
│   ├── base_implementation.py   # PydanticAI agent wrapper
│   ├── __init__.py             # Main exports
│   └── */profile.py            # Agent personalities
├── llm/
│   └── llm.py                  # PydanticAI + OpenRouter setup
└── core/
    └── config.py               # Configuration management
main.py                         # Chainlit application entry
```

### Configuration

Environment variables in `.env`:
```bash
OPENROUTER_API_KEY=your_api_key_here
MODEL_NAME=anthropic/claude-3.5-sonnet
# Add other configuration as needed
```

## 🎨 UI Customization

The application uses Chainlit with custom styling:

- **Configuration**: `.chainlit/config.toml`
- **Welcome Message**: `chainlit.md`
- **Custom Assets**: `public/` directory
- **Theming**: Supports light/dark modes

## 🔄 Workflow System

### Session Management
- **Default Agent**: Manager Agent on startup
- **Agent Persistence**: Chosen agent remains active until switched
- **Memory Integration**: Conversation history maintained across agents
- **Streaming**: Real-time response streaming for all agents

### Agent Switching Logic
```python
# Parse @ notation
if message.startswith('@'):
    agent_name = extract_agent_name(message)
    session.current_agent = agent_name
    
# Use current agent
response = await workflow.run_streaming(
    message, session.current_agent, memory
)
```

## 🧪 Development

### Adding New Agents

1. **Create agent profile**
   ```python
   # app/agents/new_agent/profile.py
   from app.core.types import AgentProfile
   
   new_agent_profile = AgentProfile(
       role="New Agent",
       goal="Specific purpose",
       backstory="Agent personality and capabilities"
   )
   ```

2. **Update workflow**
   ```python
   # Add to app/agents/workflow.py
   AGENT_PROFILES = {
       "new": new_agent_profile,
       # ... other agents
   }
   ```

3. **Export profile**
   ```python
   # Update app/agents/__init__.py
   from .new_agent.profile import new_agent_profile
   __all__.append("new_agent_profile")
   ```

### Code Quality

- **Type Safety**: Full type hints with Pydantic validation
- **Error Handling**: Comprehensive error handling and logging
- **Documentation**: Detailed docstrings and inline comments
- **Testing**: Test agent switching and streaming functionality

## 📦 Dependencies

### Core Dependencies
- **pydantic-ai-slim[openai]**: Modern AI framework
- **chainlit**: Interactive web interface
- **llama-index-core**: Memory and session management
- **pydantic**: Data validation and settings
- **python-dotenv**: Environment configuration

### Development Dependencies
- **UV**: Fast Python package manager
- **Python 3.13+**: Latest Python features

## 🚀 Deployment

### Local Development
```bash
chainlit run main.py --port 8000
```

### Production Deployment
- Configure environment variables
- Use process manager (PM2, systemd)
- Set up reverse proxy (nginx)
- Enable HTTPS for production

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-agent`
3. **Follow code standards**: Type hints, docstrings, error handling
4. **Test thoroughly**: Ensure agent switching works correctly
5. **Submit pull request**: With detailed description

### Development Guidelines

- Maintain backward compatibility
- Follow PydanticAI patterns
- Preserve session management functionality
- Update documentation for new features
- Test agent switching and streaming

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Create GitHub issues for bugs
- Use discussions for questions
- Check existing documentation

---

**Built with ❤️ using PydanticAI, Chainlit, and OpenRouter**
