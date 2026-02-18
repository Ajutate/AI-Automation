# Complete System Architecture - AI Automation

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI Automation System                         │
│                     LangGraph Workflow Orchestration              │
└─────────────────────────────────────────────────────────────────┘
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          User Interface                              │
│                                                                      │
│    CLI: main.py --brd <path> --base-name <name>                    │
│                                                                      │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      v
┌─────────────────────────────────────────────────────────────────────┐
│                      LangGraph Workflow                              │
│                     (workflow.py)                                    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                     State Management                         │  │
│  │  - brd_text: str                                            │  │
│  │  - feature_file: str                                        │  │
│  │  - selenium_test: str                                       │  │
│  │  - current_step: str                                        │  │
│  │  - messages: list                                           │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────┐          ┌──────────────────┐               │
│  │ Feature Agent    │ ────────>│ Selenium Agent   │               │
│  │ Node             │          │ Node             │               │
│  └──────────────────┘          └──────────────────┘               │
│                                                                      │
└──────────────┬───────────────────────────────┬─────────────────────┘
               │                               │
               v                               v
┌──────────────────────────────┐  ┌──────────────────────────────┐
│     Feature Agent            │  │    Selenium Agent            │
│     (agents.py)              │  │    (agents.py)               │
│                              │  │                              │
│  ┌────────────────────────┐ │  │  ┌────────────────────────┐ │
│  │ LLM: OllamaLLM        │ │  │  │ LLM: OllamaLLM        │ │
│  │ Model: qwen2.5        │ │  │  │ Model: qwen2.5        │ │
│  └────────────────────────┘ │  │  └────────────────────────┘ │
│                              │  │                              │
│  Tools:                      │  │  Tools:                      │
│  ┌────────────────────────┐ │  │  ┌────────────────────────┐ │
│  │ 1. AnalyzeBRD         │ │  │  │ 1. DesignPageObjects  │ │
│  │ 2. GenerateScenarios  │ │  │  │ 2. GenerateTestMethods│ │
│  │ 3. ValidateFeature    │ │  │  │ 3. AddSeleniumSetup   │ │
│  └────────────────────────┘ │  │  └────────────────────────┘ │
│                              │  │                              │
└──────────────┬───────────────┘  └──────────────┬───────────────┘
               │                                  │
               v                                  v
┌──────────────────────────────┐  ┌──────────────────────────────┐
│   Feature File Output        │  │   Java Test Output           │
│   (.feature)                 │  │   (.java)                    │
└──────────────────────────────┘  └──────────────────────────────┘
```

## Layer Breakdown

### 1. User Interface Layer
```
main.py
│
├─> Read BRD file
├─> Parse arguments (--brd, --base-name, --workflow, --use-strong-model)
└─> Call workflow.execute()
```

### 2. Workflow Orchestration Layer (LangGraph)
```
workflow.py
│
├─> AutomationWorkflow
│   ├─> _build_workflow()
│   │   ├─> StateGraph(AgentState)
│   │   ├─> add_node("generate_feature", feature_node)
│   │   ├─> add_node("generate_selenium", selenium_node)
│   │   ├─> add_edge("generate_feature", "generate_selenium")
│   │   └─> compile()
│   │
│   └─> execute(brd_text)
│       └─> workflow.invoke(initial_state)
│
└─> ParallelAgentWorkflow (with review steps)
    └─> Additional review nodes
```

### 3. Agent Layer (LangChain)
```
agents.py
│
├─> FeatureAgent
│   ├─> OllamaLLM (custom wrapper)
│   ├─> Tools:
│   │   ├─> AnalyzeBRD
│   │   ├─> GenerateGherkinScenarios
│   │   └─> ValidateFeature
│   │
│   └─> create_react_agent()
│
└─> SeleniumAgent
    ├─> OllamaLLM (custom wrapper)
    ├─> Tools:
    │   ├─> DesignPageObjects
    │   ├─> GenerateTestMethods
    │   └─> AddSeleniumSetup
    │
    └─> create_react_agent()
```

### 4. LLM Integration Layer
```
ollama_client.py
│
└─> generate_text()
    ├─> POST http://localhost:11434/api/generate
    ├─> Model: qwen2.5:latest / qwen2.5:7b
    └─> Returns generated text
```

### 5. Configuration Layer
```
config.py
│
└─> Config (dataclass)
    ├─> OLLAMA_BASE_URL
    ├─> OLLAMA_PRIMARY_MODEL
    ├─> OLLAMA_STRONG_MODEL
    ├─> OLLAMA_TEMPERATURE
    ├─> OLLAMA_MAX_TOKENS
    └─> Output directories
```

### 6. Prompt Engineering Layer
```
prompts.py
│
├─> FEATURE_PROMPT
│   └─> BRD → Gherkin conversion template
│
└─> JAVA_TEST_PROMPT
    └─> Feature → Selenium test template
```

## Data Flow

```
1. BRD Input (.txt)
   │
   v
2. LangGraph Workflow Initialization
   │
   v
3. Feature Agent Node Execution
   │  ├─> Analyze BRD
   │  ├─> Extract requirements
   │  ├─> Generate Gherkin
   │  └─> Validate feature
   │
   v
4. State Update (feature_file populated)
   │
   v
5. Selenium Agent Node Execution
   │  ├─> Design Page Objects
   │  ├─> Generate test methods
   │  ├─> Add setup/teardown
   │  └─> Complete test class
   │
   v
6. State Update (selenium_test populated)
   │
   v
7. Save Outputs
   │  ├─> outputs/features/<name>.feature
   │  └─> outputs/tests/<name>Test.java
   │
   v
8. Completion
```

## ReAct Pattern in Action

```
Feature Agent Reasoning:

Thought: I need to create a Gherkin feature file from this BRD
Action: AnalyzeBRD
Action Input: <brd_text>
Observation: Requirements extracted: [login, validation, error handling]

Thought: Now I have the requirements, I should generate scenarios
Action: GenerateGherkinScenarios
Action Input: <analysis_result>
Observation: Scenarios generated with Given/When/Then steps

Thought: I should validate the feature file
Action: ValidateFeature
Action Input: <generated_feature>
Observation: Valid Gherkin feature file

Thought: I now have the final answer
Final Answer: <complete_feature_file>
```

## Component Dependencies

```
main.py
    │
    ├─> ai_automation.workflow
    │   ├─> ai_automation.agents
    │   │   ├─> ai_automation.ollama_client
    │   │   ├─> ai_automation.config
    │   │   ├─> ai_automation.prompts
    │   │   ├─> langchain
    │   │   └─> langchain_core
    │   │
    │   └─> langgraph
    │
    └─> ai_automation.generator (for save_outputs)
```

## External Dependencies

```
Python Packages:
├─ requests (HTTP client for Ollama)
├─ python-dotenv (environment variables)
├─ pydantic (data validation)
├─ langchain (agent framework)
├─ langchain-core (core abstractions)
├─ langchain-community (community tools)
└─ langgraph (workflow orchestration)

External Services:
└─ Ollama (local LLM server)
   └─ Models: qwen2.5:latest, qwen2.5:7b
```

## Execution Flow Timeline

```
T0: User runs main.py
T1: BRD file loaded into memory
T2: Workflow initialized with empty state
T3: Feature Agent node invoked
T4: AnalyzeBRD tool called → Ollama generates analysis
T5: GenerateGherkinScenarios tool called → Ollama generates feature
T6: ValidateFeature tool called → Validation complete
T7: State updated with feature_file
T8: Selenium Agent node invoked
T9: DesignPageObjects tool called → Ollama generates design
T10: GenerateTestMethods tool called → Ollama generates methods
T11: AddSeleniumSetup tool called → Ollama adds setup
T12: State updated with selenium_test
T13: save_outputs() writes files to disk
T14: Process complete
```

## Error Handling Flow

```
Try:
    ├─> Read BRD
    ├─> Execute Workflow
    │   ├─> Feature Agent (with retry logic)
    │   └─> Selenium Agent (with retry logic)
    └─> Save Outputs

Except FileNotFoundError:
    └─> "BRD file not found"

Except ConnectionError:
    └─> "Ollama server not running"

Except TimeoutError:
    └─> "LLM generation timeout"
```

## Scalability Considerations

```
Current: Single BRD → Single Feature → Single Test
Future Enhancements:
├─> Batch processing (multiple BRDs)
├─> Parallel agent execution
├─> Agent collaboration
├─> Human-in-the-loop validation
├─> Continuous learning
└─> Multi-model ensemble
```

---

This architecture provides:
- ✅ Clear separation of concerns
- ✅ Easy to extend with new agents
- ✅ Tool-based modularity
- ✅ State management
- ✅ Professional workflow orchestration
