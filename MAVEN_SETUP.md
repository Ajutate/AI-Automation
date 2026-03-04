# Maven Auto-Setup Guide

## Overview

The AI-Automation framework now includes **complete automation** for Maven project setup and dependency resolution. No more manual configuration!

## ✨ What Gets Automated

1. **Maven Project Structure Creation**
   - Standard `src/test/java` and `src/test/resources` layout
   - Proper package structure (`com.automation`)
   - `pom.xml` with all Cucumber, Selenium, JUnit dependencies

2. **File Organization**
   - Copies all generated `.java` test files to `src/test/java/com/automation/`
   - Copies all `.feature` files to `src/test/resources/features/`
   - Cleans markdown formatting from generated files automatically

3. **Dependency Resolution** (if Maven installed)
   - Downloads all required JAR files
   - Resolves transitive dependencies
   - Caches dependencies in local Maven repository

4. **VS Code Integration**
   - Updates `.vscode/settings.json` with Java classpath
   - Configures source paths for Java language server
   - Sets up automatic build configuration

## 🚀 Usage

### Option 1: CLI with Auto-Setup

```bash
python main.py --brd data/brd_sample.txt --base-name MyTest --auto-setup-maven
```

This single command:
- Generates feature files
- Generates Java test code
- Sets up Maven project
- Resolves dependencies
- Compiles tests

### Option 2: Standalone Setup

Generate first, then setup:

```bash
# Step 1: Generate tests
python main.py --brd data/brd_sample.txt --base-name MyTest

# Step 2: Run setup
python setup_project.py
```

### Option 3: Web UI

1. Start the server: `python app.py`
2. Open browser: `http://localhost:8000`
3. Upload BRD file
4. Check ✅ "Auto-setup Maven project & resolve dependencies"
5. Click "Generate Tests"

Or use the dedicated endpoint:
```bash
curl -X POST http://localhost:8000/setup-maven
```

## 📋 Prerequisites

### Required
- **Java JDK 11+**: For compiling tests
- **Python 3.8+**: For running the automation

### Optional
- **Maven 3.6+**: For dependency resolution and test execution
  - If Maven is not installed, the setup will still work but skip dependency resolution
  - You can install Maven later and run `mvn dependency:resolve` manually

### Installing Maven

**Windows:**
```powershell
# Automated installation
.\install_maven.ps1

# Then restart terminal
mvn --version
```

**Linux/Mac:**
```bash
# Automated installation
chmod +x install_maven.sh
./install_maven.sh

# Update PATH
source ~/.bashrc  # or ~/.zshrc

# Verify
mvn --version
```

**Manual Installation:**
1. Download from: https://maven.apache.org/download.cgi
2. Extract to a directory (e.g., `C:\maven` or `~/maven`)
3. Add `<maven-dir>/bin` to your PATH
4. Restart terminal and verify: `mvn --version`

## 📁 Generated Project Structure

After running the auto-setup, you'll have:

```
test-project/
├── pom.xml                                    # Maven configuration
│   ├── Dependencies: Cucumber 7.15.0
│   ├── Dependencies: Selenium 4.16.1
│   ├── Dependencies: JUnit 5.10.1
│   └── Plugins: surefire, compiler
│
├── src/
│   ├── main/java/com/automation/            # (Optional) Shared utilities
│   └── test/
│       ├── java/com/automation/             # All test .java files
│       │   ├── MyTestStepDefinitions.java
│       │   ├── MyTestRunner.java
│       │   └── ...
│       └── resources/features/              # All .feature files
│           ├── MyTest.feature
│           └── ...
│
└── target/
    ├── classes/                              # Compiled code
    ├── test-classes/                         # Compiled tests
    ├── surefire-reports/                     # Test results
    └── site/                                 # HTML reports
```

## ⚙️ VS Code Configuration

The setup automatically creates/updates `.vscode/settings.json`:

```json
{
    "java.project.referencedLibraries": [
        "test-project/target/**/*.jar",
        ".m2/repository/**/*.jar"
    ],
    "java.project.sourcePaths": [
        "test-project/src/main/java",
        "test-project/src/test/java"
    ],
    "java.project.outputPath": "test-project/target/classes",
    "java.configuration.updateBuildConfiguration": "automatic"
}
```

**After auto-setup:**
1. Reload VS Code: `Ctrl+Shift+P` → "Reload Window"
2. Java language server will automatically:
   - Detect the Maven project
   - Load all dependencies
   - Enable code completion, error detection, etc.

## 🔍 Troubleshooting

### No compilation errors but dependencies not resolved

**Cause**: Maven not installed

**Solution**:
```bash
# Install Maven
.\install_maven.ps1      # Windows
# or
./install_maven.sh        # Linux/Mac

# Then run setup again
python setup_project.py
```

### VS Code still shows errors

**Cause**: Java language server needs reload

**Solution**:
1. Press `Ctrl+Shift+P`
2. Type "Java: Clean Java Language Server Workspace"
3. Restart VS Code
4. Or: `Ctrl+Shift+P` → "Reload Window"

### Files still have markdown formatting

**Cause**: Old generated files

**Solution**:
```bash
# Re-run setup (it cleans files automatically)
python setup_project.py

# Or regenerate from scratch
python main.py --brd data/brd_sample.txt --base-name MyTest --auto-setup-maven
```

### Maven build fails with "package does not exist"

**Cause**: Wrong package structure

**Solution**:
- All test files should be in `com.automation` package
- Check if files have: `package com.automation;` at the top
- Make sure files are in: `src/test/java/com/automation/`

## 🎯 Benefits

### Before Auto-Setup (Manual)
1. ❌ Generate tests
2. ❌ Manually create Maven project structure
3. ❌ Manually copy files to correct locations
4. ❌ Manually create pom.xml with dependencies
5. ❌ Run `mvn dependency:resolve`
6. ❌ Configure VS Code manually
7. ❌ Run `mvn clean compile`
8. ❌ Fix any errors
9. ✅ Finally run tests

**Time: ~15-30 minutes per project**

### After Auto-Setup (Automated)
1. ✅ Generate tests with `--auto-setup-maven` flag

**Time: ~2-3 minutes (depending on internet speed for dependencies)**

## 🔗 Integration with CI/CD

The auto-setup can be integrated into your CI/CD pipeline:

```bash
# In Jenkinsfile or GitHub Actions
python main.py --brd $BRD_FILE --base-name $TEST_NAME --auto-setup-maven
cd test-project
mvn clean test
```

See [CICD.md](CICD.md) for complete CI/CD integration examples.

## 🎉 Summary

With the Maven auto-setup feature, you get:

✅ **Zero manual configuration** - Everything is automated  
✅ **Clean generated code** - Markdown formatting removed automatically  
✅ **VS Code ready** - Java language server configured  
✅ **Dependencies resolved** - All JARs downloaded  
✅ **Compilation verified** - Tests compile successfully  
✅ **Ready to run** - Execute tests with `mvn test`

**One command, complete automation!** 🚀
