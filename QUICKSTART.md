# Quick Start Guide: Agentic AI Automation

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Ensure Ollama is Running

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start Ollama
ollama serve
```

### Step 3: Pull Required Models

```bash
ollama pull qwen2.5:latest
# Or for better quality:
ollama pull qwen2.5:7b
```

### Step 4: Run the Agentic Workflow

```bash
python main.py --brd data/brd_sample.txt --base-name TestAutomation
```

## 📖 What Happens?

### The Workflow:

```
1. 📄 BRD Input
   └─> Reads your business requirements

2. 🤖 Feature Agent (First Agent)
   ├─> Analyzes BRD
   ├─> Extracts requirements
   └─> Generates Gherkin feature file

3. 🔄 State Transfer
   └─> Passes feature file to next agent

4. 🤖 Selenium Agent (Second Agent)
   ├─> Designs Page Objects
   ├─> Creates test methods
   └─> Generates complete Java tests

5. 💾 Output
   ├─> outputs/features/TestAutomation.feature
   └─> outputs/tests/TestAutomationTest.java
```

## 🎯 Example BRD

Create a file `my_brd.txt`:

```
Business Requirement: User Login

The system shall allow users to login with email and password.

Requirements:
1. User enters email address
2. User enters password
3. System validates credentials
4. On success, user is redirected to dashboard
5. On failure, error message is displayed

Validation Rules:
- Email must be valid format
- Password must be at least 8 characters
- Max 3 failed attempts before lockout
```

## ⚡ Run It

```bash
python main.py --brd my_brd.txt --base-name UserLogin --use-strong-model
```

## 🎉 Results

You'll get:

1. **Feature File** (`outputs/features/UserLogin.feature`):
```gherkin
Feature: User Login
  Scenario: Successful login
    Given I am on the login page
    When I enter valid credentials
    Then I should be redirected to dashboard
```

2. **Java Test** (`outputs/tests/UserLoginTest.java`):
```java
@Test
public void testSuccessfulLogin() {
    LoginPage loginPage = new LoginPage(driver);
    loginPage.enterEmail("user@example.com");
    loginPage.enterPassword("password123");
    loginPage.clickLogin();
    // assertions...
}
```

## 🔧 Workflow Options

### Standard Workflow (Default)
```bash
python main.py --brd my_brd.txt
```
Sequential execution: Feature Agent → Selenium Agent

### Enhanced Workflow (With Reviews)
```bash
python main.py --brd my_brd.txt --workflow parallel
```
Adds validation steps between agents

### High-Quality Mode
```bash
python main.py --brd my_brd.txt --use-strong-model
```
Uses more powerful LLM for better output

## 🛠️ Troubleshooting

### Ollama Not Running
```bash
# Error: Connection refused
# Solution:
ollama serve
```

### Model Not Found
```bash
# Error: model 'qwen2.5:latest' not found
# Solution:
ollama pull qwen2.5:latest
```

### Import Errors
```bash
# Error: No module named 'langgraph'
# Solution:
pip install -r requirements.txt
```

## 📚 Next Steps

1. **Customize Agents**: Edit `ai_automation/agents.py`
2. **Add Tools**: Extend agent capabilities
3. **Custom Workflows**: Modify `ai_automation/workflow.py`
4. **Integrate**: Use as library in your projects

## 💡 Pro Tips

- Use `--use-strong-model` for production-quality output
- Start with small BRDs to test the workflow
- Check `outputs/` directory for generated files
- Use `--workflow parallel` for quality review steps

---

**Ready to automate? Run your first workflow now! 🚀**
