# AI-Automation: Agentic BRD to Automation Framework

## 🚀 Overview

This project implements an **Agentic AI solution** using **LangGraph** and **LangChain** to automatically generate:
1. **Gherkin Feature Files** from Business Requirements Documents (BRD)
2. **Selenium WebDriver Tests** in Java from the generated feature files

## 🏗️ Architecture

### Agentic System Design

The system uses **two specialized agents** orchestrated by **LangGraph**:

```
┌─────────────────────────────────────────────────────────┐
│                    LangGraph Workflow                    │
│                                                          │
│  ┌────────────┐       ┌──────────────┐                 │
│  │    BRD     │──────>│ Feature Agent│─────┐            │
│  │   Input    │       │              │     │            │
│  └────────────┘       └──────────────┘     │            │
│                              │              │            │
│                              │              v            │
│                              │      ┌──────────────┐    │
│                              │      │   Feature    │    │
│                              │      │    File      │    │
│                              │      └──────────────┘    │
│                              │              │            │
│                              │              v            │
│                              │      ┌──────────────┐    │
│                              └─────>│   Selenium   │    │
│                                     │    Agent     │    │
│                                     └──────────────┘    │
│                                            │             │
│                                            v             │
│                                     ┌──────────────┐    │
│                                     │  Java Tests  │    │
│                                     └──────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### Agent Descriptions

#### 1. **Feature Agent** 🎯
- **Responsibility**: Convert BRD into Gherkin feature files
- **Tools**:
  - `AnalyzeBRD`: Extracts requirements and user stories
  - `GenerateGherkinScenarios`: Creates Gherkin scenarios
  - `ValidateFeature`: Validates syntax and completeness
- **Output**: Properly structured `.feature` files with Given/When/Then steps

#### 2. **Selenium Agent** 🤖
- **Responsibility**: Generate Selenium WebDriver automation tests
- **Tools**:
  - `DesignPageObjects`: Creates Page Object Model structure
  - `GenerateTestMethods`: Generates JUnit 5 test methods
  - `AddSeleniumSetup`: Adds WebDriver setup/teardown
- **Output**: Production-ready Java test classes using Selenium WebDriver

## 📦 Installation

### Prerequisites
- Python 3.8+
- Ollama running locally (default: http://localhost:11434)
- Ollama models: `qwen2.5:latest` or `qwen2.5:7b`

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Verify Ollama is running
curl http://localhost:11434/api/tags
```

## 🎮 Usage

### Usage Examples

```bash
# Standard sequential workflow
python main.py --brd data/brd_sample.txt --base-name MyFeature

# Use stronger model for better quality
python main.py --brd data/brd_sample.txt --base-name MyFeature --use-strong-model

# Enhanced workflow with review steps
python main.py --brd data/brd_sample.txt --base-name MyFeature --workflow parallel
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
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── ai_automation/
│   ├── __init__.py
│   ├── config.py            # Configuration management
│   ├── prompts.py           # Prompt templates
│   ├── ollama_client.py     # Ollama API client
│   ├── generator.py         # Output utilities
│   ├── agents.py            # LangChain agent definitions ⭐
│   └── workflow.py          # LangGraph workflow orchestration ⭐
├── data/
│   └── brd_sample.txt       # Sample BRD input
└── outputs/
    ├── features/            # Generated .feature files
    └── tests/              # Generated Java test files
```

## 🌟 Key Features

### Agentic Implementation

1. **LangGraph Orchestration**: State-based workflow management
2. **Specialized Agents**: Separate agents for feature and test generation
3. **Tool-based Architecture**: Each agent has specialized tools
4. **ReAct Pattern**: Agents use Thought-Action-Observation loops
5. **State Management**: Shared state across workflow nodes

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

- **LangChain**: Agent framework and LLM integration
- **LangGraph**: Workflow orchestration and state management
- **Ollama**: Local LLM inference
- **Python**: Core language
- **Gherkin/BDD**: Feature file format
- **Selenium WebDriver**: Test automation framework
- **JUnit 5**: Java testing framework

## 🚧 Advanced Usage

### Custom Agents

You can extend the agents by adding more tools:

```python
from langchain.tools import Tool

new_tool = Tool(
    name="CustomTool",
    func=your_function,
    description="Description of what the tool does"
)

feature_agent.tools.append(new_tool)
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

1. **Initialize State**: Load BRD text
2. **Feature Agent Execution**:
   - Analyze BRD requirements
   - Generate Gherkin scenarios
   - Validate feature file
3. **State Transfer**: Pass feature to next agent
4. **Selenium Agent Execution**:
   - Design Page Objects
   - Generate test methods
   - Add Selenium setup
5. **Output**: Save both feature and test files

## 🤝 Contributing

To add new capabilities:

1. Define new tools in `agents.py`
2. Update workflow in `workflow.py`
3. Add prompts in `prompts.py`

## 📝 License

MIT License

## 🔗 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Ollama](https://ollama.ai/)
- [Selenium WebDriver](https://www.selenium.dev/)
- [Gherkin Reference](https://cucumber.io/docs/gherkin/)

---

**Built with ❤️ using LangGraph and LangChain**
