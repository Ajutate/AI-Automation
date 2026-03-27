"""Agent definitions using langchain.agents.create_agent.

Uses ChatOpenAI (pointing to LiteLLM proxy) as the model — no custom wrapper classes.
Requires langchain>=1.0.1 and langchain-core>=1.2.14.
"""

from typing import List, Tuple
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from .config import Config
from .tools import (
    compile_java_code,
    validate_feature_syntax,
    check_java_dependencies,
    analyze_code_quality,
)


def _make_llm(model_name: str, cfg: 'Config') -> ChatOpenAI:
    """Instantiate ChatOpenAI pointing to the local LiteLLM proxy."""
    return ChatOpenAI(
        model_name=model_name,
        api_key=cfg.litellm_api_key,
        base_url=cfg.litellm_base_url,
        temperature=cfg.temperature,
    )



def create_feature_agent(use_strong_model: bool = True):
    """Create a langchain agent for Gherkin feature file generation.

    Returns a compiled agent graph (CompiledStateGraph) and the model name.
    Invoke with: agent.invoke({"messages": [{"role": "user", "content": brd_text}]})
    """
    cfg = Config()
    model_name = cfg.strong_model if use_strong_model else cfg.primary_model
    llm = _make_llm(model_name, cfg)

    system_prompt = """You are a senior QA analyst specializing in BDD/Gherkin.
Your task is to create high-quality Gherkin feature files from Business Requirements Documents.

When given a BRD, generate a complete Gherkin feature file following these STRICT rules:

RULE 1 - USE DataTable FOR FORM/FIELD DATA:
Whenever a step involves filling in form fields (name, email, password, address, etc.),
put the data in an inline DataTable directly under the step. Example:

  When the user fills in the registration form
    | First Name | John             |
    | Last Name  | Doe              |
    | Email      | john@example.com |
    | Password   | P@ssw0rd123      |

RULE 2 - USE Scenario Outline FOR MULTIPLE DATA SETS:
Whenever a scenario should run with multiple sets of input (valid/invalid emails, etc.),
use Scenario Outline with an Examples table. Example:

  Scenario Outline: Login with different credentials
    When the user logs in with "<email>" and "<password>"
    Then the result is "<result>"

    Examples:
      | email            | password    | result  |
      | john@example.com | P@ssw0rd123 | success |
      | wrong@test.com   | wrongpass   | failure |

RULE 3 - NEVER write steps like "the user enters a valid email and password"
without providing the actual values in a DataTable or Scenario Outline. The step
must carry the data — do not leave data undefined.

RULE 4 - ALWAYS detect intents from latest customer email ONLY.
When the input contains a thread or history of multiple customer emails,
extract requirements and intents exclusively from the most recent email.
Ignore all prior emails in the thread.

Generate:
- Feature description
- Background (if needed) for shared preconditions only
- Multiple Scenarios using DataTable for form data
- At least one Scenario Outline with Examples for parameterized cases
- At least one negative test case

Output ONLY the Gherkin feature file content, no explanations."""

    agent = create_agent(
        model=llm,
        tools=None,
        system_prompt=system_prompt,
    )
    return agent, model_name


def create_selenium_agent(use_strong_model: bool = True):
    """Create a langchain agent for Cucumber step definitions generation.

    Returns a compiled agent graph (CompiledStateGraph) and the model name.
    Invoke with: agent.invoke({"messages": [{"role": "user", "content": feature_text}]})
    """
    cfg = Config()
    model_name = cfg.strong_model if use_strong_model else cfg.primary_model
    llm = _make_llm(model_name, cfg)

    system_prompt = """You are a senior QA automation engineer specializing in Cucumber BDD, Selenium WebDriver, and Java.
Your task is to create production-ready Cucumber step definitions from Gherkin feature files.

Generate a complete Java step definitions class with:
- Cucumber annotations (@Given, @When, @Then, @And)
- WebDriver setup in @Before hook, teardown in @After hook
- Page Object Model pattern
- Selenium WebDriver interactions
- JUnit assertions
- All required imports

=== HOW TO READ DATA FROM THE FEATURE FILE ===

1. DATATABLE STEPS
When a Gherkin step is followed by a | table |, the Java method receives a DataTable.
Read values using dataTable.asMap():

  // Feature file:
  //   When the user fills in the registration form
  //     | First Name | John             |
  //     | Email      | john@example.com |
  //     | Password   | P@ssw0rd123      |

  @When("the user fills in the registration form")
  public void theUserFillsInTheRegistrationForm(DataTable dataTable) {
      Map<String, String> data = dataTable.asMap(String.class, String.class);
      registerPage.enterFirstName(data.get("First Name"));
      registerPage.enterEmail(data.get("Email"));
      registerPage.enterPassword(data.get("Password"));
  }

2. SCENARIO OUTLINE PARAMETERS
When a step uses <placeholder> or {string}, Cucumber passes it as a method argument:

  // Feature file:
  //   When the user logs in with "john@example.com" and "P@ssw0rd123"

  @When("the user logs in with {string} and {string}")
  public void theUserLogsInWith(String email, String password) {
      loginPage.enterEmail(email);
      loginPage.enterPassword(password);
  }

3. ABSOLUTE RULE — NEVER HARDCODE TEST DATA
NEVER write values like this inside a method body:
  String email = "john@example.com";  // WRONG - hardcoded
  String password = "P@ssw0rd123";    // WRONG - hardcoded
ALL data must come from DataTable or method parameters above.

=== REQUIRED IMPORTS ===
import io.cucumber.java.en.*;
import io.cucumber.java.Before;
import io.cucumber.java.After;
import io.cucumber.datatable.DataTable;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import java.util.Map;

Class name must end with "StepDefinitions".
Output ONLY the Java code, no explanations."""

    agent = create_agent(
        model=llm,
        tools=None,
        system_prompt=system_prompt,
    )
    return agent, model_name


def create_validation_agent(use_strong_model: bool = True):
    """Create a langchain agent for code validation with tools.

    Returns a compiled agent graph (CompiledStateGraph), the model name, and the tools list.
    Invoke with: agent.invoke({"messages": [{"role": "user", "content": code_text}]})
    """
    cfg = Config()
    model_name = cfg.strong_model if use_strong_model else cfg.primary_model
    llm = _make_llm(model_name, cfg)

    validation_tools = [
        compile_java_code,
        validate_feature_syntax,
        check_java_dependencies,
        analyze_code_quality,
    ]

    system_prompt = """You are a senior QA validation engineer and code reviewer.
Your task is to validate generated test code for correctness, quality, and executability.

You have access to the following tools:
- compile_java_code: Compile Java code to check for syntax errors
- validate_feature_syntax: Validate Gherkin feature file syntax
- check_java_dependencies: Check if Java code has proper imports and dependencies
- analyze_code_quality: Analyze code metrics and quality

When validating code:
1. First validate the feature file syntax
2. Then analyze feature file quality metrics
3. Check Java code dependencies
4. Compile the Java code to verify it's syntactically correct
5. Analyze Java code quality metrics
6. Provide a comprehensive validation report

Use the tools to perform actual validation, not just visual inspection.
Provide specific, actionable feedback if issues are found."""

    agent = create_agent(
        model=llm,
        tools=validation_tools,
        system_prompt=system_prompt,
    )
    return agent, model_name, validation_tools
