# AI-Automation: Agentic BRD to Automation Framework

## 🚀 Overview

This project implements an **Agentic AI solution** using **LangGraph** and **LangChain** to automatically generate:
1. **Gherkin Feature Files** from Business Requirements Documents (BRD)
2. **Selenium WebDriver Tests** in Java from the generated feature files

**Two Interfaces Available:**
- **CLI**: Command-line interface for automation/CI-CD
- **Web UI**: FastAPI-based browser interface with file upload

## 🏗️ Architecture

### Agentic System Design

The system uses **two specialized agents** orchestrated by **LangGraph StateGraph**:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     LangGraph StateGraph Workflow                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────┐                                                    │
│  │   BRD/JIRA  │                                                    │
│  │   Document  │                                                    │
│  │ (.txt/.docx │                                                    │
│  │    /.pdf)   │                                                    │
│  └──────┬──────┘                                                    │
│         │                                                            │
│         v                                                            │
│  ┌─────────────────────────────────────────────┐                   │
│  │         Workflow Node: Feature Generation    │                   │
│  ├─────────────────────────────────────────────┤                   │
│  │  • Invokes Feature Agent                    │                   │
│  │  • Agent: langchain.agents.create_agent     │                   │
│  │  • System Prompt: QA/BDD Expert             │                   │
│  │  • LLM Backend: Ollama (qwen2.5)            │                   │
│  └───────────────────┬─────────────────────────┘                   │
│                      │                                               │
│                      v                                               │
│              ┌───────────────┐                                      │
│              │  AgentState   │                                      │
│              │ {feature_file}│                                      │
│              └───────┬───────┘                                      │
│                      │                                               │
│                      v                                               │
│  ┌─────────────────────────────────────────────┐                   │
│  │       Workflow Node: Test Generation         │                   │
│  ├─────────────────────────────────────────────┤                   │
│  │  • Invokes Selenium Agent                   │                   │
│  │  • Agent: langchain.agents.create_agent     │                   │
│  │  • System Prompt: Selenium/Java Expert      │                   │
│  │  • LLM Backend: Ollama (qwen2.5)            │                   │
│  └───────────────────┬─────────────────────────┘                   │
│                      │                                               │
│                      v                                               │
│              ┌───────────────┐                                      │
│              │  AgentState   │                                      │
│              │{selenium_test}│                                      │
│              └───────┬───────┘                                      │
│                      │                                               │
│                      v                                               │
│              ┌───────────────┐                                      │
│              │  Save Files   │                                      │
│              │   • .feature  │                                      │
│              │   • .java     │                                      │
│              └───────────────┘                                      │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘

        ┌──────────────────────────────────────────┐
        │      Technical Implementation Details      │
        ├──────────────────────────────────────────┤
        │  • LangGraph: StateGraph orchestration   │
        │  • LangChain: create_agent() for agents  │
        │  • Ollama: Local LLM inference           │
        │  • State: Immutable dict passed between  │
        │           nodes with agent outputs       │
        │  • No Tool Calling: Direct prompting     │
        │                     (Ollama limitation)  │
        └──────────────────────────────────────────┘
```

**Key Components:**

1. **LangGraph StateGraph**: Manages workflow execution and state transitions
2. **Agent Nodes**: Workflow nodes that invoke LangChain agents
3. **Agent State**: Shared state dict containing BRD text, feature file, and test code
4. **System Prompts**: Pre-configured prompts defining agent expertise
5. **Ollama Backend**: Local LLM (qwen2.5) for agent inference

### Agent Descriptions

#### 1. **Feature Agent** 🎯
- **Responsibility**: Convert BRD into Gherkin feature files
- **Created with**: `langchain.agents.create_agent` (official LangChain API)
- **System Prompt**: Expert QA analyst specializing in BDD/Gherkin
- **Output**: Properly structured `.feature` files with Given/When/Then steps
- **Features**:
  - Analyzes requirements and user stories
  - Generates multiple scenarios with Given/When/Then steps
  - Includes negative test cases
  - Validates Gherkin syntax

#### 2. **Selenium Agent** 🤖
- **Responsibility**: Generate Selenium WebDriver automation tests
- **Created with**: `langchain.agents.create_agent` (official LangChain API)
- **System Prompt**: Expert QA automation engineer specializing in Selenium/Java
- **Output**: Production-ready Java test classes using Selenium WebDriver
- **Features**:
  - Designs Page Object Model structure
  - Generates JUnit 5 test methods with assertions
  - Adds WebDriver setup/teardown
  - Produces clean, production-ready code

**Note**: Agents use direct prompting (Ollama doesn't support native tool calling)

## 📦 Installation

### Prerequisites
- Python 3.8+
- Ollama running locally (default: http://localhost:11434)
- Ollama models: `qwen2.5:latest` or `qwen2.5:7b`

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Dependencies include:
# - langchain, langgraph (agentic framework)
# - fastapi, uvicorn (web server)
# - python-docx, PyPDF2 (document processing)
# - requests (Ollama API client)

# Verify Ollama is running
curl http://localhost:11434/api/tags

# Pull required models (if not already available)
ollama pull qwen2.5:latest
ollama pull qwen2.5:7b
```

## 🎮 Usage

### Option 1: Web UI (Recommended for Manual Testing)

```bash
# Start the FastAPI server
python app.py

# Open browser to http://localhost:8000
# Upload BRD file (.txt, .docx, .pdf)
# Configure options and generate tests
# Download generated files
```

**Web UI Features:**
- Drag & drop file upload
- Real-time generation status
- In-browser preview of generated files
- Direct download buttons
- Support for .txt, .docx, and .pdf formats

### Option 2: CLI (Recommended for Automation/CI-CD)

```bash
# Standard sequential workflow
python main.py --brd data/brd_sample.txt --base-name MyFeature

# Use stronger model for better quality
python main.py --brd data/brd_sample.txt --base-name MyFeature --use-strong-model

# Enhanced workflow with review steps
python main.py --brd data/brd_sample.txt --base-name MyFeature --workflow parallel

# Example with JIRA story
python main.py --brd data/jira_story_sample.txt --base-name UserLogin --use-strong-model
```

## 🔧 Configuration

Environment variables (optional):

```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_PRIMARY_MODEL=qwen2.5:latest
OLLAMA_STRONG_MODEL=qwen2.5:7b
OLLAMA_TEMPERATURE=0.2
OLLAMA_MAX_TOKENS=2048
OLLAMA_TIMEOUT_S=120

# Output Directories
OUTPUT_FEATURE_DIR=outputs/features
OUTPUT_TEST_DIR=outputs/tests
```

## 📁 Project Structure

```
AI-Automation/
├── main.py                  # CLI entry point
├── app.py                   # FastAPI web application ⭐
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── ai_automation/
│   ├── __init__.py
│   ├── config.py            # Configuration management
│   ├── prompts.py           # System prompt templates
│   ├── ollama_client.py     # Ollama API client (with logging)
│   ├── generator.py         # Output file utilities
│   ├── agents.py            # LangChain agent creation ⭐
│   └── workflow.py          # LangGraph workflow orchestration ⭐
├── static/
│   └── index.html           # Web UI frontend
├── data/
│   ├── brd_sample.txt       # Sample BRD
│   ├── jira_story_sample.txt # Sample JIRA story
│   └── jira_story_cart.txt  # Sample shopping cart story
├── outputs/
│   ├── features/            # Generated .feature files
│   └── tests/              # Generated Java test files
└── temp/                    # Temporary upload directory
```

## 🌟 Key Features

### Agentic Implementation

1. **LangGraph Orchestration**: State-based workflow management
2. **Official LangChain Agents**: Uses `langchain.agents.create_agent` (not deprecated APIs)
3. **Specialized Agent Roles**: Separate agents for feature and test generation
4. **System Prompt-Based**: Agents guided by detailed system prompts
5. **State Management**: Shared state across workflow nodes
6. **Automatic Cleanup**: Removes markdown code fences from LLM output

### Additional Features

- **LLM Call Logging**: Tracks Ollama API calls with prompt/response sizes
- **Multiple Input Formats**: Supports .txt, .docx, and .pdf files
- **Dual Interface**: Web UI for manual use, CLI for automation
- **Configurable Models**: Choose between default and strong models
- **Validation Steps**: Optional parallel workflow with review nodes
- **Production Ready**: Clean output without markdown artifacts

### Workflow Types

#### Standard Workflow
```
BRD → Feature Agent → Feature File → Selenium Agent → Java Tests
```

#### Parallel Workflow (with Reviews)
```
BRD → Feature Agent → Feature Review → Selenium Agent → Test Review → Java Tests
```

## 🔍 Example Output

### Feature File (`.feature`)
```gherkin
Feature: Online Account Opening
  As a potential customer
  I want to open an account online
  So that I can start using banking services

  Scenario: Successful account opening
    Given I am on the account opening page
    When I fill in valid personal information
    And I submit the application
    Then I should see a confirmation message
    And my account should be created
```

### Java Test (`.java`)
```java
@Test
public void testSuccessfulAccountOpening() {
    driver.get("https://bank.com/open-account");
    // Page Object and WebDriver interactions
    // Assertions
}
```

## 🛠️ Technology Stack

**Backend:**
- **LangChain**: Agent framework and LLM integration (`langchain.agents.create_agent`)
- **LangGraph**: Workflow orchestration and state management
- **FastAPI**: Web API framework
- **Uvicorn**: ASGI server
- **Ollama**: Local LLM inference (qwen2.5 models)
- **Python 3.8+**: Core language

**Output Frameworks:**
- **Gherkin/BDD**: Feature file format
- **Selenium WebDriver**: Generated test automation framework
- **JUnit 5**: Generated Java testing framework

**Document Processing:**
- **python-docx**: Word document reading
- **PyPDF2**: PDF document reading

## 🚧 Advanced Usage

### Custom System Prompts

You can customize agent behavior by modifying system prompts in `ai_automation/agents.py`:

```python
def create_feature_agent(use_strong_model: bool = True):
    system_prompt = """Your custom prompt here..."""
    
    agent = create_agent(
        model=llm,
        tools=None,
        system_prompt=system_prompt
    )
    return agent
```

### Custom Workflows

Create your own workflow by extending `StateGraph`:

```python
from langgraph.graph import StateGraph, END
from ai_automation.workflow import AgentState

workflow = StateGraph(AgentState)
workflow.add_node("custom_node", your_function)
workflow.set_entry_point("custom_node")
workflow.add_edge("custom_node", END)
compiled_workflow = workflow.compile()
```

## 📊 Workflow Visualization

The agentic workflow follows this execution pattern:

### Standard Workflow Execution Flow:

```
1. User Input (CLI or Web UI)
   ↓
2. Initialize AgentState
   {
     "brd_text": "User story content...",
     "feature_file": "",
     "selenium_test": "",
     "current_step": "start",
     "messages": []
   }
   ↓
3. LangGraph StateGraph.invoke(initial_state)
   ↓
4. Node 1: _generate_feature_node()
   • Creates agent: feature_agent = create_agent(llm, system_prompt=QA_EXPERT)
   • Invokes agent: result = feature_agent.invoke({"messages": [{"role": "user", "content": brd_text}]})
   • Agent calls Ollama LLM via HTTP POST
   • Ollama generates Gherkin feature file
   • Cleans markdown code fences
   • Updates state: state["feature_file"] = cleaned_output
   ↓
5. LangGraph passes updated state to next node
   ↓
6. Node 2: _generate_selenium_node()
   • Creates agent: selenium_agent = create_agent(llm, system_prompt=SELENIUM_EXPERT)
   • Invokes agent: result = selenium_agent.invoke({"messages": [{"role": "user", "content": feature_file}]})
   • Agent calls Ollama LLM via HTTP POST
   • Ollama generates Java Selenium test
   • Cleans markdown code fences
   • Updates state: state["selenium_test"] = cleaned_output
   ↓
7. LangGraph reaches END node
   ↓
8. Return final state to caller
   ↓
9. Save files to outputs/ directory
   • outputs/features/{base_name}.feature
   • outputs/tests/{base_name}Test.java
```

### Parallel Workflow (with validation):

Adds review nodes between generation steps:
```
Feature Generation → Feature Validation → Selenium Generation → Test Validation
```

**Validation checks:**
- Feature files: Verifies "Feature:" and "Scenario:" keywords exist
- Test files: Structural validation of generated code

### Key Implementation Details:

1. **Agent Creation**: Agents are instantiated when workflow is initialized
2. **Agent Invocation**: Each workflow node invokes its agent with current state
3. **LLM Calls**: 2 HTTP calls to Ollama (one per agent)
4. **State Immutability**: Each node returns new state dict (functional pattern)
5. **Cleanup**: Markdown code fences removed from LLM output
6. **Logging**: All LLM calls logged with prompt/response sizes

## 🤝 Contributing

To add new capabilities:

1. Define new agents in `agents.py` using `create_agent()`
2. Update workflow in `workflow.py`
3. Modify system prompts in `agents.py`
4. For web UI: Update `app.py` and `static/index.html`

## 🐛 Troubleshooting

**Ollama not responding:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama (if not running)
ollama serve
```

**Port 8000 already in use:**
```bash
# Find and kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

**Import errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

**LLM not generating properly:**
- Check Ollama is running and models are downloaded
- Increase timeout in `config.py` (default: 120s)
- Try using `--use-strong-model` flag for better quality

## 📝 License

MIT License

## 🔗 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Ollama](https://ollama.ai/)
- [Selenium WebDriver](https://www.selenium.dev/)
- [Gherkin Reference](https://cucumber.io/docs/gherkin/)
- [JUnit 5](https://junit.org/junit5/)

---

**Built with ❤️ using LangGraph, LangChain, and FastAPI**
