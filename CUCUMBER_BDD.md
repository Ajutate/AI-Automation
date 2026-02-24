# Cucumber BDD Implementation Guide

## Overview

The system now generates **proper Cucumber BDD test automation** that binds Gherkin feature files to Java step definitions for execution.

## Generated Files

For each test scenario, the system generates **3 interconnected files**:

### 1. Feature File (`.feature`)
**Location**: `outputs/features/TestName.feature`

**Purpose**: Contains Gherkin scenarios describing test behavior in natural language

**Example**:
```gherkin
Feature: Online Account Opening

  Scenario: Valid account opening process
    Given a customer named John who is 20 years old
    When John starts the account opening process
    Then he provides his personal details
    And the system creates the account
```

### 2. Step Definitions (`.java`)
**Location**: `outputs/tests/TestNameStepDefinitions.java`

**Purpose**: Java class implementing each Gherkin step with Selenium WebDriver code

**Key Annotations**:
- `@Given` - Setup/preconditions
- `@When` - Actions/events
- `@Then` - Assertions/outcomes
- `@Before` - WebDriver initialization
- `@After` - WebDriver cleanup

**Example**:
```java
import io.cucumber.java.en.*;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class AccountOpeningStepDefinitions {
    
    private WebDriver driver;
    
    @Before
    public void setUp() {
        driver = new ChromeDriver();
    }
    
    @Given("a customer named {string} who is {int} years old")
    public void customerWithAge(String name, int age) {
        // Implementation with WebDriver
    }
    
    @When("John starts the account opening process")
    public void startAccountOpening() {
        driver.get("http://example.com/account-opening");
        // More WebDriver code...
    }
    
    @After
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
```

### 3. Test Runner (`.java`)
**Location**: `outputs/tests/TestNameRunner.java`

**Purpose**: Binds feature files to step definitions and configures test execution

**Example**:
```java
import org.junit.runner.RunWith;
import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;

@RunWith(Cucumber.class)
@CucumberOptions(
    features = "src/test/resources/features",
    glue = {"stepdefinitions"},
    plugin = {
        "pretty",
        "html:target/cucumber-reports/cucumber.html",
        "json:target/cucumber-reports/cucumber.json"
    },
    monochrome = true
)
public class AccountOpeningRunner {
    // This class remains empty - Cucumber uses annotations
}
```

## How They Bind Together

### Execution Flow

```
┌─────────────────┐
│ Feature File    │
│ (Gherkin)       │
└────────┬────────┘
         │
         │ Cucumber matches steps via regex/expressions
         ▼
┌─────────────────┐
│ Test Runner     │──┐
│ @RunWith        │  │
│ @CucumberOptions│  │ Finds and binds
└─────────────────┘  │
                     │
                     ▼
┌─────────────────────────────────┐
│ Step Definitions               │
│ @Given, @When, @Then           │
│ Contains Selenium WebDriver    │
└─────────────────────────────────┘
```

### Binding Mechanism

1. **Runner discovers features**: 
   - `features = "src/test/resources/features"` tells Cucumber where to find `.feature` files

2. **Runner discovers step definitions**:
   - `glue = {"stepdefinitions"}` tells Cucumber which package contains step definition classes

3. **Cucumber matches steps**:
   - For each Gherkin step, Cucumber uses **regex/Cucumber expressions** to find matching Java method
   - Example: `@Given("a customer named {string}")` matches `Given a customer named John`

4. **Execution**:
   - Cucumber reads each scenario
   - Executes Java methods in the order defined by Gherkin
   - WebDriver performs actual browser automation

## Project Structure

For Cucumber to work properly, organize files like this:

```
project/
├── src/
│   ├── test/
│   │   ├── java/
│   │   │   ├── stepdefinitions/
│   │   │   │   └── *StepDefinitions.java  ← Step definitions here
│   │   │   └── runners/
│   │   │       └── *Runner.java           ← Test runners here
│   │   └── resources/
│   │       └── features/
│   │           └── *.feature              ← Feature files here
│   └── main/
│       └── java/
│           └── pageobjects/               ← Page Objects (optional)
└── pom.xml                                ← Cucumber dependencies
```

## Dependencies

The `cicd/pom.xml` includes all required dependencies:

```xml
<!-- Cucumber Core -->
<dependency>
    <groupId>io.cucumber</groupId>
    <artifactId>cucumber-java</artifactId>
    <version>7.15.0</version>
</dependency>

<!-- Cucumber JUnit Runner -->
<dependency>
    <groupId>io.cucumber</groupId>
    <artifactId>cucumber-junit</artifactId>
    <version>7.15.0</version>
    <scope>test</scope>
</dependency>

<!-- Selenium WebDriver -->
<dependency>
    <groupId>org.seleniumhq.selenium</groupId>
    <artifactId>selenium-java</artifactId>
    <version>4.16.1</version>
</dependency>

<!-- JUnit 4 (required by Cucumber) -->
<dependency>
    <groupId>junit</groupId>
    <artifactId>junit</artifactId>
    <version>4.13.2</version>
</dependency>
```

## Running Tests

### Option 1: Maven Command Line
```bash
# Run all Cucumber tests
mvn test

# Run specific runner
mvn test -Dtest=AccountOpeningRunner

# Generate reports only
mvn test -Dcucumber.options="--dry-run"
```

### Option 2: IDE (IntelliJ/Eclipse)
1. Right-click on `*Runner.java` class
2. Select "Run As → JUnit Test"
3. Cucumber executes all scenarios in linked feature file

### Option 3: CI/CD Pipeline
```yaml
- name: Run Cucumber Tests
  run: |
    cd cicd
    mvn clean test
    
- name: Publish Cucumber Reports
  uses: actions/upload-artifact@v3
  with:
    name: cucumber-reports
    path: cicd/target/cucumber-reports/
```

## Reports

Cucumber generates multiple report formats:

1. **HTML Report**: `target/cucumber-reports/cucumber.html`
   - Visual report with pass/fail status
   - Screenshots (if configured)
   - Execution time

2. **JSON Report**: `target/cucumber-reports/cucumber.json`
   - Machine-readable format
   - For CI/CD dashboards

3. **JUnit XML**: `target/cucumber-reports/cucumber.xml`
   - Compatible with Jenkins, TeamCity, etc.

## Matching Steps to Methods

### Exact Text Match
```gherkin
Given a customer logs in
```
```java
@Given("a customer logs in")
public void customerLogsIn() { }
```

### With Parameters
```gherkin
Given a customer named "John"
```
```java
@Given("a customer named {string}")
public void customerNamed(String name) { }
```

### With Multiple Parameters
```gherkin
Given a customer "John" aged 25
```
```java
@Given("a customer {string} aged {int}")
public void customerWithAge(String name, int age) { }
```

### Regex Match (Advanced)
```gherkin
Given I have 5 cucumbers in my basket
```
```java
@Given("^I have (\\d+) cucumbers in my basket$")
public void cucumbersInBasket(int count) { }
```

## Workflow Types

The system supports 3 workflow modes (all generate Cucumber BDD files):

### 1. Standard Workflow
- Generates feature file → step definitions → runner
- No validation

### 2. Parallel Workflow (with Reviews)
- Generates feature file
- ✓ Validates feature syntax
- Generates step definitions & runner
- ✓ Validates Java syntax

### 3. Tools Workflow (with Execution)
- Generates feature file
- ✓ **Validates with tools** (actual syntax checking)
- Generates step definitions & runner
- ✓ **Compiles Java code** (actual compilation)
- ✓ **Analyzes code quality** (metrics)

## Web UI Usage

1. **Upload BRD document** (TXT, PDF, DOCX)
2. **Enter test name** (e.g., "AccountOpening")
3. **Select workflow type**:
   - Standard (fastest)
   - Parallel (with reviews)
   - Tools (with validation & compilation)
4. **Click "Generate Tests"**
5. **Download 3 files**:
   - Feature file
   - Step definitions
   - Test runner

## CLI Usage

```bash
# Generate Cucumber BDD tests
python main.py --brd data/brd_sample.txt --base-name AccountOpening --workflow standard

# Output:
# ✓ outputs/features/AccountOpening.feature
# ✓ outputs/tests/AccountOpeningStepDefinitions.java
# ✓ outputs/tests/AccountOpeningRunner.java
```

## Advantages of Cucumber BDD

### ✅ **True BDD** - Feature files define behavior, step definitions implement it
### ✅ **Reusable Steps** - Same step definition works across multiple scenarios
### ✅ **Business-Readable** - Non-technical stakeholders can read and validate scenarios
### ✅ **Maintainable** - Changes to implementation don't affect feature files
### ✅ **Comprehensive Reports** - Built-in HTML/JSON reporting
### ✅ **IDE Support** - IntelliJ/Eclipse plugins provide step navigation

## Troubleshooting

### Issue: "Undefined step"
**Cause**: Gherkin step doesn't match any `@Given/@When/@Then` method

**Fix**: 
1. Check regex/expression in step definition
2. Ensure `glue` path in runner points to step definitions package

### Issue: "No features found"
**Cause**: Runner can't find `.feature` files

**Fix**:
1. Check `features` path in `@CucumberOptions`
2. Ensure feature files are in `src/test/resources/features/`

### Issue: "WebDriver not initialized"
**Cause**: WebDriver setup missing or failed

**Fix**:
1. Check `@Before` hook initializes WebDriver
2. Ensure ChromeDriver/GeckoDriver in PATH
3. Use WebDriverManager dependency for automatic driver management

## Next Steps

1. **Generate tests**: Use web UI or CLI
2. **Organize files**: Place in proper Maven structure
3. **Run tests**: Execute via Maven or IDE
4. **View reports**: Open HTML report in browser
5. **Iterate**: Update feature files and regenerate step definitions

For more information, see:
- [Cucumber Documentation](https://cucumber.io/docs)
- [Selenium Java Documentation](https://www.selenium.dev/documentation/)
- `CICD.md` for CI/CD integration
