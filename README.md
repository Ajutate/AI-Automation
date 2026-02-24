# AI-Automation: Agentic BRD to Cucumber BDD Framework

## 🚀 Overview

This project implements an **Agentic AI solution** using **LangGraph** and **LangChain** to automatically generate **complete Cucumber BDD test automation** from Business Requirements Documents:

### Generated Output (3 Files):
1. **Gherkin Feature Files** (`.feature`) - Business-readable test scenarios
2. **Cucumber Step Definitions** (`.java`) - Selenium WebDriver implementation with `@Given/@When/@Then` annotations
3. **Cucumber Test Runner** (`.java`) - JUnit runner that binds features to step definitions for execution

**Key Innovation**: Unlike traditional code generators, this creates **true BDD tests** where Gherkin scenarios are executable specifications that directly drive Selenium automation.

**Two Interfaces Available:**
- **CLI**: Command-line interface for automation/CI-CD
- **Web UI**: FastAPI-based browser interface with drag-drop file upload

## 🏗️ Architecture

### Agentic System Design - Cucumber BDD Generation

The system uses **two specialized agents** orchestrated by **LangGraph StateGraph** to generate complete Cucumber BDD test suites:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     LangGraph StateGraph Workflow                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────┐                                                            │
│  │   BRD/JIRA  │                                                            │
│  │   Document  │                                                            │
│  │ (.txt/.docx │                                                            │
│  │    /.pdf)   │                                                            │
│  └──────┬──────┘                                                            │
│         │                                                                    │
│         v                                                                    │
│  ┌─────────────────────────────────────────────────────┐                   │
│  │       Workflow Node: Feature Generation              │                   │
│  ├─────────────────────────────────────────────────────┤                   │
│  │  • Invokes Feature Agent (BDD Expert)               │                   │
│  │  • Agent: langchain.agents.create_agent             │                   │
│  │  • System Prompt: QA/BDD/Gherkin Expert             │                   │
│  │  • LLM Backend: Ollama (qwen2.5)                    │                   │
│  │  • Output: Gherkin scenarios with Given/When/Then   │                   │
│  └───────────────────┬─────────────────────────────────┘                   │
│                      │                                                       │
│                      v                                                       │
│              ┌───────────────────┐                                          │
│              │   AgentState      │                                          │
│              │  {feature_file:   │                                          │
│              │   "Feature:..."}  │                                          │
│              └───────┬───────────┘                                          │
│                      │                                                       │
│                      │ [OPTIONAL: Validation Node with Tools]               │
│                      │ • validate_feature_syntax()                          │
│                      │ • analyze_code_quality()                             │
│                      │                                                       │
│                      v                                                       │
│  ┌─────────────────────────────────────────────────────┐                   │
│  │     Workflow Node: Cucumber Step Definitions         │                   │
│  ├─────────────────────────────────────────────────────┤                   │
│  │  • Invokes Selenium Agent (Cucumber Expert)         │                   │
│  │  • Agent: langchain.agents.create_agent             │                   │
│  │  • System Prompt: Cucumber BDD + Selenium Expert    │                   │
│  │  • LLM Backend: Ollama (qwen2.5)                    │                   │
│  │  • Output 1: Step definitions with @Given/@When/    │                   │
│  │              @Then + Selenium WebDriver code        │                   │
│  │  • Output 2: Cucumber runner class with             │                   │
│  │              @RunWith + @CucumberOptions            │                   │
│  └───────────────────┬─────────────────────────────────┘                   │
│                      │                                                       │
│                      v                                                       │
│              ┌───────────────────┐                                          │
│              │   AgentState      │                                          │
│              │ {step_definitions,│                                          │
│              │  runner_class}    │                                          │
│              └───────┬───────────┘                                          │
│                      │                                                       │
│                      │ [OPTIONAL: Tools Validation Node]                    │
│                      │ • compile_java_code() - ACTUAL javac                 │
│                      │ • check_java_dependencies()                          │
│                      │ • analyze_code_quality()                             │
│                      │                                                       │
│                      v                                                       │
│              ┌────────────────────┐                                         │
│              │   Save 3 Files     │                                         │
│              │  • .feature        │                                         │
│              │  • *StepDefs.java  │                                         │
│              │  • *Runner.java    │                                         │
│              └────────────────────┘                                         │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘

        ┌────────────────────────────────────────────────────────┐
        │         How Cucumber BDD Binding Works                  │
        ├────────────────────────────────────────────────────────┤
        │                                                          │
        │  1. Runner discovers:                                   │
        │     features = "src/test/resources/features"            │
        │     glue = {"stepdefinitions"}                          │
        │                                                          │
        │  2. Cucumber reads Gherkin scenarios                    │
        │                                                          │
        │  3. For each step, Cucumber matches via regex:          │
        │     Gherkin: "Given a customer named John"              │
        │         ↓ (matches)                                     │
        │     Java: @Given("a customer named {string}")           │
        │                                                          │
        │  4. Cucumber invokes Java method with parameters        │
        │                                                          │
        │  5. Selenium WebDriver executes browser automation      │
        │                                                          │
        │  6. Assertions validate behavior                        │
        │                                                          │
        │  7. Reports generated (HTML/JSON/XML)                   │
        │                                                          │
        └────────────────────────────────────────────────────────┘

        ┌──────────────────────────────────────────┐
        │   Technical Implementation Details        │
        ├──────────────────────────────────────────┤
        │  • LangGraph: StateGraph orchestration   │
        │  • LangChain: create_agent() for agents  │
        │  • Ollama: Local LLM inference           │
        │  • State: Immutable dict passed between  │
        │           nodes with agent outputs       │
        │  • Tools: Optional code validation &     │
        │           compilation via subprocess     │
        │  • Cucumber: JUnit runner binds Gherkin  │
        │              to Java step definitions    │
        └──────────────────────────────────────────┘
```

**Key Components:**

1. **LangGraph StateGraph**: Manages workflow execution and state transitions
2. **Agent Nodes**: Workflow nodes that invoke LangChain agents
3. **Agent State**: Shared state dict containing BRD text, feature file, step definitions, and runner
4. **System Prompts**: Pre-configured prompts defining agent expertise (BDD + Cucumber)
5. **Ollama Backend**: Local LLM (qwen2.5) for agent inference
6. **Validation Tools**: Optional executable tools for code compilation and syntax validation

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

#### 2. **Selenium Agent (Cucumber Expert)** 🤖
- **Responsibility**: Generate Cucumber step definitions and test runner
- **Created with**: `langchain.agents.create_agent` (official LangChain API)
- **System Prompt**: Expert QA automation engineer specializing in Cucumber BDD, Selenium WebDriver, and Java
- **Output**: Two Java files:
  1. **Step Definitions Class** (`*StepDefinitions.java`):
     - Cucumber annotations: `@Given`, `@When`, `@Then`, `@And`
     - Regex/Cucumber expressions matching Gherkin steps
     - Selenium WebDriver implementation
     - `@Before` hook for WebDriver initialization
     - `@After` hook for cleanup
     - Page Object Model design
  2. **Test Runner Class** (`*Runner.java`):
     - `@RunWith(Cucumber.class)` annotation
     - `@CucumberOptions` binding features to step definitions
     - Report configuration (HTML, JSON, XML)
- **Features**:
  - Maps each Gherkin step to Java method
  - Implements browser automation with Selenium
  - Includes proper assertions
  - Generates clean, production-ready code
  - Creates executable BDD test suite

#### 3. **Validation Agent (Optional)** 🔧
- **Responsibility**: Validate generated code using executable tools
- **Created with**: `langchain.agents.create_agent` with bound tools
- **Always enabled**: Code validation with compilation
- **Tools**:
  - `compile_java_code()` - Actual javac compilation
  - `validate_feature_syntax()` - Gherkin keyword validation
  - `check_java_dependencies()` - Import validation
  - `analyze_code_quality()` - Code metrics (LOC, methods)
  - `run_maven_test()` - Execute Maven test runs
- **Features**:
  - Validates before saving files
  - Returns actual compilation errors
  - Ensures generated code is syntactically correct

**Implementation Notes**:
- Feature & Selenium agents use **direct prompting** (Ollama limitation)
- Validation agent uses **tool-calling** via LangChain's tool framework
- Tools execute via subprocess for actual validation

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
- Three workflow modes: Standard, Parallel (review), Tools (validation)
- In-browser preview of all 3 generated files
- Direct download buttons for each file
- Support for .txt, .docx, and .pdf formats

**Generated Files (3):**
1. **Feature File** (`.feature`) - Gherkin scenarios
2. **Step Definitions** (`*StepDefinitions.java`) - Cucumber implementation
3. **Test Runner** (`*Runner.java`) - Binds features to step definitions

### Option 2: CLI (Recommended for Automation/CI-CD)

```bash
# Standard workflow - generates Cucumber BDD tests
python main.py --brd data/brd_sample.txt --base-name AccountOpening

# Use stronger model for better quality
python main.py --brd data/brd_sample.txt --base-name AccountOpening --use-strong-model

# Example with JIRA story
python main.py --brd data/jira_story_sample.txt --base-name UserLogin --use-strong-model
```

**Output:**
```
✓ outputs/features/AccountOpening.feature
✓ outputs/tests/AccountOpeningStepDefinitions.java
✓ outputs/tests/AccountOpeningRunner.java
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
├── main.py                      # CLI entry point
├── app.py                       # FastAPI web application ⭐
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── CUCUMBER_BDD.md              # Cucumber BDD implementation guide ⭐
├── CICD.md                      # CI/CD integration guide
├── ai_automation/
│   ├── __init__.py
│   ├── config.py                # Configuration management
│   ├── ollama_client.py         # Ollama API client (with logging)
│   ├── generator.py             # Output file utilities (3-file support) ⭐
│   ├── agents.py                # LangChain agent creation (Cucumber expertise) ⭐
│   ├── workflow.py              # LangGraph workflow orchestration ⭐
│   ├── tools.py                 # Validation tools (compile, validate, analyze) ⭐
│   └── cucumber_runner.py       # Cucumber runner generation utility
├── static/
│   └── index.html               # Web UI frontend (3-file download) ⭐
├── cicd/
│   ├── pom.xml                  # Maven config with Cucumber dependencies ⭐
│   ├── run_generated_tests.sh  # Linux/Mac test execution script
│   └── run_generated_tests.ps1 # Windows test execution script
├── .github/workflows/
│   └── test-generation-cicd.yml # GitHub Actions CI/CD
├── Jenkinsfile                  # Jenkins pipeline configuration
├── Dockerfile                   # Container image for deployment
├── data/
│   ├── brd_sample.txt           # Sample BRD
│   ├── jira_story_sample.txt    # Sample JIRA story
│   └── jira_story_cart.txt      # Sample shopping cart story
├── outputs/
│   ├── features/                # Generated .feature files
│   └── tests/                   # Generated Java files:
│       ├── *StepDefinitions.java  # Cucumber step definitions ⭐
│       └── *Runner.java           # Cucumber test runners ⭐
└── temp/                        # Temporary upload directory
```

**⭐ New/Updated for Cucumber BDD**

## 🌟 Key Features

### Cucumber BDD Generation

1. **Complete Test Suite Generation**: Creates 3 interconnected files that work together
2. **True BDD**: Feature files are executable specifications, not just documentation
3. **Step Definition Binding**: Automatic generation of `@Given/@When/@Then` annotations with regex matching
4. **Selenium Integration**: Step definitions contain Selenium WebDriver implementation
5. **Test Runner Creation**: Generates JUnit runner with `@CucumberOptions` binding
6. **Reusable Steps**: Same step definition methods work across multiple scenarios
7. **Business Readable**: Gherkin scenarios understandable by non-technical stakeholders

### Agentic Implementation

1. **LangGraph Orchestration**: State-based workflow management with nodes and edges
2. **Official LangChain Agents**: Uses `langchain.agents.create_agent` (modern API)
3. **Specialized Agent Roles**: Separate agents for feature generation and Cucumber implementation
4. **System Prompt-Based**: Agents guided by detailed expert personas
5. **State Management**: Immutable state passed between workflow nodes
6. **Automatic Cleanup**: Removes markdown code fences from LLM output

### Validation & Quality

1. **Tool-Enabled Validation** (optional): 
   - `compile_java_code()` - Actual javac compilation
   - `validate_feature_syntax()` - Gherkin keyword validation
   - `check_java_dependencies()` - Import checking
   - `analyze_code_quality()` - Code metrics analysis
2. **LLM Call Logging**: Tracks Ollama API calls with prompt/response sizes
3. **Multiple Workflow Modes**: Standard, parallel (with reviews), tools (with validation)
4. **Error Detection**: Catches compilation errors before saving files

### Additional Features

- **Multiple Input Formats**: Supports .txt, .docx, and .pdf files
- **Dual Interface**: Web UI for manual use, CLI for automation
- **Configurable Models**: Choose between default and strong LLM models
- **CI/CD Integration**: GitHub Actions, Jenkins, Docker support
- **Production Ready**: Clean output without markdown artifacts
- **Report Generation**: Cucumber HTML/JSON/XML reports

## 🔍 Example Output

### Input: Business Requirement Document
```text
User Story: Online Account Opening
As a customer, I want to open a bank account online
so that I can start using banking services.

Acceptance Criteria:
- Customer provides personal details (name, DOB, address)
- System validates KYC documentation
- Account is created with unique account number
- Customer receives confirmation email
```

### Output 1: Feature File (`.feature`)
```gherkin
Feature: Online Account Opening (Retail Banking)

  Background:
    Given a customer named John who is 20 years old
    And the bank's KYC service is available
    And the core banking system is operational

  Scenario: Valid account opening process
    When John starts the account opening process via the web channel
    Then he provides his personal details (name, DOB, address, phone, email)
    And he uploads his ID proof and address proof
    When the KYC verification is successful
    Then he selects a savings account type and submits the application
    And the system creates the account in the core banking system
    And John receives an account number
    And John receives a confirmation email and SMS

  Scenario: Invalid KYC due to OTP mismatch
    Given John has started the account opening process via the web channel
    When he provides his personal details
    And the OTP for his phone number is sent but not verified correctly
    Then an error message is shown asking to verify the OTP again
    And John's application is rejected
```

### Output 2: Step Definitions Java File (`*StepDefinitions.java`)
```java
import io.cucumber.java.en.*;
import io.cucumber.java.Before;
import io.cucumber.java.After;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.WebDriverWait;
import static org.junit.Assert.*;

public class OnlineAccountOpeningStepDefinitions {
    
    private WebDriver driver;
    private String customerName;
    private String accountNumber;
    
    @Before
    public void setUp() {
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
        driver = new ChromeDriver();
    }
    
    @Given("a customer named {string} who is {int} years old")
    public void customerWithAge(String name, int age) {
        this.customerName = name;
        driver.get("http://example.com/account-opening");
    }
    
    @Given("the bank's KYC service is available")
    public void kycServiceAvailable() {
        // Mock or verify KYC service endpoint
        assertTrue(driver.findElement(By.id("kyc-service-status")).isDisplayed());
    }
    
    @When("{string} starts the account opening process via the web channel")
    public void startsAccountOpening(String name) {
        driver.findElement(By.id("start-application")).click();
    }
    
    @Then("he provides his personal details \\(name, DOB, address, phone, email\\)")
    public void providesPersonalDetails() {
        driver.findElement(By.id("name")).sendKeys(customerName);
        driver.findElement(By.id("dob")).sendKeys("01/01/2000");
        driver.findElement(By.id("address")).sendKeys("123 Main St");
        driver.findElement(By.id("phone")).sendKeys("555-0123");
        driver.findElement(By.id("email")).sendKeys("john@example.com");
    }
    
    @Then("he uploads his ID proof and address proof")
    public void uploadsDocuments() {
        driver.findElement(By.id("id-proof")).sendKeys("/path/to/id.pdf");
        driver.findElement(By.id("address-proof")).sendKeys("/path/to/address.pdf");
    }
    
    @When("the KYC verification is successful")
    public void kycVerificationSuccessful() {
        driver.findElement(By.id("verify-kyc")).click();
        WebDriverWait wait = new WebDriverWait(driver, 10);
        wait.until(d -> d.findElement(By.id("kyc-status")).getText().equals("Verified"));
    }
    
    @Then("the system creates the account in the core banking system")
    public void accountCreatedInCoreSystem() {
        assertTrue(driver.findElement(By.id("account-created")).isDisplayed());
    }
    
    @Then("{string} receives an account number")
    public void receivesAccountNumber(String name) {
        accountNumber = driver.findElement(By.id("account-number")).getText();
        assertNotNull(accountNumber);
        assertFalse(accountNumber.isEmpty());
    }
    
    @Then("{string} receives a confirmation email and SMS")
    public void receivesConfirmation(String name) {
        assertTrue(driver.findElement(By.id("email-sent")).isDisplayed());
        assertTrue(driver.findElement(By.id("sms-sent")).isDisplayed());
    }
    
    @After
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
```

### Output 3: Test Runner Java File (`*Runner.java`)
```java
import org.junit.runner.RunWith;
import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;

/**
 * Cucumber Test Runner for Online Account Opening
 * 
 * This class binds Gherkin feature files to Java step definitions.
 * Run this class to execute all scenarios in the feature file.
 */
@RunWith(Cucumber.class)
@CucumberOptions(
    features = "src/test/resources/features",
    glue = {"stepdefinitions"},
    plugin = {
        "pretty",
        "html:target/cucumber-reports/cucumber.html",
        "json:target/cucumber-reports/cucumber.json",
        "junit:target/cucumber-reports/cucumber.xml"
    },
    monochrome = true,
    dryRun = false
)
public class OnlineAccountOpeningRunner {
    // This class remains empty - Cucumber uses annotations to run tests
}
```

### How They Connect

**Execution Flow:**
```
1. Run OnlineAccountOpeningRunner.java
2. JUnit invokes Cucumber via @RunWith annotation
3. Cucumber reads @CucumberOptions:
   - features: finds .feature file
   - glue: finds step definition classes
4. Cucumber parses Gherkin scenarios
5. For each step, Cucumber matches via regex:
   "Given a customer named John" 
       ↓ (matches)
   @Given("a customer named {string}")
6. Cucumber invokes Java method with parameter "John"
7. Selenium WebDriver executes browser automation
8. Assertions validate expected behavior
9. Cucumber generates HTML/JSON/XML reports
```

## 🛠️ Technology Stack

**AI/Agent Framework:**
- **LangChain 1.2.10**: Agent framework and LLM integration (`langchain.agents.create_agent`)
- **LangGraph 1.0.8**: Workflow orchestration and state management
- **Ollama**: Local LLM inference (qwen2.5:latest, qwen2.5:7b)

**Backend:**
- **FastAPI 0.129.0**: Web API framework
- **Uvicorn**: ASGI server
- **Python 3.8+**: Core language

**BDD Testing Framework:**
- **Cucumber 7.15.0**: BDD test execution framework
- **Gherkin**: Feature file format (Given/When/Then)
- **Selenium WebDriver 4.16.1**: Browser automation
- **JUnit 5.10.1**: Test runner (via Cucumber)
- **Maven 3.9**: Build and dependency management

**Code Validation Tools:**
- **javac**: Java compiler (for validation workflow)
- **subprocess**: Tool execution
- **Maven**: Test compilation and execution

**Document Processing:**
- **python-docx**: Word document reading
- **PyPDF2**: PDF document reading

**CI/CD:**
- **GitHub Actions**: Automated test generation pipeline
- **Jenkins**: Pipeline configuration with Jenkinsfile
- **Docker**: Container-based deployment

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

The agentic workflow follows this execution pattern for Cucumber BDD generation:

### Standard Workflow Execution Flow:

```
1. User Input (CLI or Web UI)
   ↓
2. Initialize AgentState
   {
     "brd_text": "User story content...",
     "feature_file": "",
     "step_definitions": "",
     "runner_class": "",
     "current_step": "start",
     "messages": []
   }
   ↓
3. LangGraph StateGraph.invoke(initial_state)
   ↓
4. Node 1: _generate_feature_node()
   • Creates agent: feature_agent = create_agent(llm, system_prompt=BDD_EXPERT)
   • Invokes agent: result = feature_agent.invoke({"messages": [{"role": "user", "content": brd_text}]})
   • Agent calls Ollama LLM via HTTP POST
   • Ollama generates Gherkin feature file with scenarios
   • Cleans markdown code fences
   • Updates state: state["feature_file"] = cleaned_gherkin
   ↓
5. [OPTIONAL] Validation Node (tools workflow only)
   • Validation agent uses tools:
     - validate_feature_syntax(feature_file)
     - analyze_code_quality(feature_file)
   • Results stored in state["validation_results"]["feature"]
   ↓
6. LangGraph passes updated state to next node
   ↓
7. Node 2: _generate_selenium_node()
   • Creates agent: selenium_agent = create_agent(llm, system_prompt=CUCUMBER_EXPERT)
   • Invokes agent: result = selenium_agent.invoke({"messages": [{"role": "user", "content": feature_file}]})
   • Agent calls Ollama LLM via HTTP POST
   • Ollama generates:
     a) Cucumber step definitions with @Given/@When/@Then
     b) Selenium WebDriver implementation
     c) @Before/@After hooks for WebDriver setup/cleanup
   • Cleans markdown code fences
   • Updates state: state["step_definitions"] = cleaned_java
   • Generates runner: state["runner_class"] = generate_cucumber_runner(feature_file)
     - Creates JUnit runner with @RunWith(Cucumber.class)
     - Adds @CucumberOptions with features/glue paths
     - Configures report plugins
   ↓
8. [OPTIONAL] Validation Node (tools workflow only)
   • Validation agent uses tools:
     - compile_java_code(step_definitions) - ACTUAL javac compilation
     - check_java_dependencies(step_definitions)
     - analyze_code_quality(step_definitions)
   • Results stored in state["validation_results"]["selenium"]
   ↓
9. LangGraph reaches END node
   ↓
10. Return final state to caller
   ↓
11. Save 3 files to outputs/ directory
   • outputs/features/{base_name}.feature
   • outputs/tests/{base_name}StepDefinitions.java
   • outputs/tests/{base_name}Runner.java
```

### Workflow Architecture

The system uses a **single, optimized workflow** with direct tool validation:

```
BRD → Feature Agent → Direct Tool Validation → Gherkin File 
    → Selenium Agent → Direct Tool Compilation → Step Definitions + Runner
```

**Key Features:**
- **Fast**: Direct tool calls (no agent loops)
- **Validated**: Actual javac compilation + syntax checking
- **Output**: 3 files (feature, step definitions, runner) + validation reports

**Validation checks performed:**
- ✅ Feature files: Gherkin keyword validation, structure analysis
- ✅ Step definitions: **Actual Java compilation** with javac, import checking, code metrics
- ✅ **Optimized**: Tools called directly (not through agent), reducing LLM calls from 15+ to just 2
- Real-time feedback on compilation errors before saving files

### Key Implementation Details:

1. **Agent Creation**: Agents instantiated when workflow initializes
2. **Agent Invocation**: Each workflow node invokes its agent with current state
3. **LLM Calls**: 2 HTTP calls to Ollama (one for feature, one for step definitions)
4. **Runner Generation**: Programmatically created (not LLM-generated) for consistency
5. **State Immutability**: Each node returns new state dict (functional pattern)
6. **Cleanup**: Markdown code fences removed from LLM output
7. **Tool Execution**: Subprocess-based validation (javac, syntax checkers)
8. **Logging**: All LLM calls logged with prompt/response sizes

### Cucumber BDD Binding Process

After generation, when tests are executed:

```
1. User runs: AccountOpeningRunner.java
   ↓
2. JUnit sees @RunWith(Cucumber.class)
   ↓
3. Control transfers to Cucumber framework
   ↓
4. Cucumber reads @CucumberOptions:
   - features = "src/test/resources/features"  → finds .feature files
   - glue = {"stepdefinitions"}                → finds step definition classes
   ↓
5. Cucumber parses Gherkin from feature file
   ↓
6. For each Gherkin step:
   "Given a customer named John"
        ↓ Cucumber regex matching
   @Given("a customer named {string}")
        ↓
   Method: customerNamed(String name)
   ↓
7. Cucumber invokes Java method with parameters
   ↓
8. Selenium WebDriver executes browser automation
   ↓
9. Assertions validate expected behavior
   ↓
10. Cucumber generates reports (HTML/JSON/XML)
```

## 🔄 CI/CD Integration

### Automated Test Compilation & Execution

The generated Cucumber BDD tests can be automatically compiled and executed in your CI/CD pipeline.

#### Quick Start

**Local execution (Windows):**
```powershell
# Generate Cucumber BDD tests
python main.py --brd data/brd_sample.txt --base-name AccountOpening

# Compile and run with Maven
cd cicd
mvn clean test
```

**Local execution (Linux/Mac):**
```bash
# Generate Cucumber BDD tests
python main.py --brd data/brd_sample.txt --base-name AccountOpening

# Compile and run with Maven
cd cicd
mvn clean test
```

#### Running Cucumber Tests

**Prerequisites:**
1. Organize generated files in Maven structure:
```
project/
├── src/test/
│   ├── java/
│   │   ├── stepdefinitions/
│   │   │   └── AccountOpeningStepDefinitions.java
│   │   └── runners/
│   │       └── AccountOpeningRunner.java
│   └── resources/
│       └── features/
│           └── AccountOpening.feature
└── pom.xml (from cicd/ directory)
```

2. Install dependencies:
```bash
mvn clean install
```

**Execution Methods:**

1. **Run via Maven:**
```bash
mvn test
```

2. **Run via IDE (IntelliJ/Eclipse):**
- Right-click `AccountOpeningRunner.java`
- Select "Run As → JUnit Test"

3. **Run specific scenarios:**
```bash
mvn test -Dcucumber.options="--tags @smoke"
```

**Test Reports:**
- **HTML Report**: `target/cucumber-reports/cucumber.html`
- **JSON Report**: `target/cucumber-reports/cucumber.json`
- **JUnit XML**: `target/cucumber-reports/cucumber.xml`

#### CI/CD Platforms

**GitHub Actions** (Automatic on push):
- Workflow: [`.github/workflows/test-generation-cicd.yml`](.github/workflows/test-generation-cicd.yml)
- Triggers on BRD updates in `data/` folder
- Stages: Generate → Organize → Compile → Execute → Report
- Publishes Cucumber HTML reports as artifacts

**Jenkins Pipeline**:
- Configuration: [`Jenkinsfile`](Jenkinsfile)
- Parameterized builds for different BRDs
- Cucumber HTML reports with pass/fail metrics
- Email notifications

**Docker**:
```bash
# Build image with Cucumber dependencies
docker build -t ai-test-automation .

# Generate and run Cucumber tests
docker run -v $(pwd)/outputs:/app/outputs \
           ai-test-automation generate \
           --brd data/brd_sample.txt --base-name AccountOpening
```

#### Pipeline Stages

1. **Generate** - AI creates feature files, step definitions, and runner
2. **Organize** - Places files in Maven structure
3. **Compile** - Maven compiles Java code (validates syntax)
4. **Execute** - Runs Cucumber tests with Selenium ChromeDriver
5. **Report** - Generates and publishes Cucumber HTML/JSON reports

**📖 Full CI/CD documentation**: See [CICD.md](CICD.md) for:
- GitHub Actions setup
- Jenkins configuration
- GitLab CI/Azure DevOps examples
- Docker deployment
- Troubleshooting guide

**📖 Cucumber BDD Guide**: See [CUCUMBER_BDD.md](CUCUMBER_BDD.md) for:
- How Gherkin binds to Java step definitions
- Step matching with Cucumber expressions
- Page Object Model implementation
- Report configuration
- Best practices

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

**Cucumber: "Undefined step" error:**
```
Cause: Gherkin step doesn't match any @Given/@When/@Then method
Fix:
1. Check regex/expression in step definition
2. Ensure glue path in runner points to step definitions package
3. Verify step definition class is in correct package
```

**Cucumber: "No features found" error:**
```
Cause: Runner can't locate .feature files
Fix:
1. Check features path in @CucumberOptions
2. Ensure feature files are in src/test/resources/features/
3. Verify Maven structure is correct
```

**Compilation errors in generated code:**
```
**Solution**: Code is automatically validated and compiled during generation
Solution 2: Check Maven dependencies in cicd/pom.xml
Solution 3: Regenerate with --use-strong-model flag
```

**WebDriver not found:**
```bash
# Option 1: Add WebDriverManager dependency (already in pom.xml)
# Option 2: Set chromedriver path manually
export PATH=$PATH:/path/to/chromedriver

# Option 3: Use WebDriverManager in code (auto-download)
WebDriverManager.chromedriver().setup();
```

## 📝 License

MIT License

## 🔗 Resources

**AI & Agent Frameworks:**
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Ollama](https://ollama.ai/)

**BDD & Testing:**
- [Cucumber Documentation](https://cucumber.io/docs/cucumber/)
- [Gherkin Reference](https://cucumber.io/docs/gherkin/reference/)
- [Cucumber Best Practices](https://cucumber.io/docs/bdd/)
- [Selenium WebDriver](https://www.selenium.dev/)
- [JUnit 5](https://junit.org/junit5/)

**Web Framework:**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

**Project Guides:**
- [CUCUMBER_BDD.md](CUCUMBER_BDD.md) - How Cucumber binding works
- [CICD.md](CICD.md) - CI/CD integration guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture details

---

**Built with ❤️ using LangGraph, LangChain, Cucumber, and Selenium**
