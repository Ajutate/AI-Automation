# CI/CD Integration Guide

This guide explains how to integrate the AI test generation tool into your CI/CD pipeline.

## Table of Contents
- [Overview](#overview)
- [GitHub Actions](#github-actions)
- [Jenkins](#jenkins)
- [Docker](#docker)
- [Local Execution](#local-execution)
- [GitLab CI](#gitlab-ci)
- [Azure DevOps](#azure-devops)

## Overview

The CI/CD pipeline performs the following steps:
1. **Generate Tests**: Use AI to generate Gherkin features and Java Selenium tests from BRD
2. **Compile Tests**: Compile the generated Java code using Maven
3. **Execute Tests**: Run Selenium tests with ChromeDriver
4. **Generate Reports**: Create test execution reports

## GitHub Actions

### Setup

The workflow is defined in [`.github/workflows/test-generation-cicd.yml`](.github/workflows/test-generation-cicd.yml).

### Usage

**Automatic trigger** (on push to main/develop):
```bash
git add data/new_brd.txt
git commit -m "Add new BRD"
git push origin main
```

**Manual trigger**:
1. Go to Actions tab in GitHub
2. Select "Generate and Run Selenium Tests"
3. Click "Run workflow"
4. Specify BRD file and test name

### Configuration

Required secrets: None (uses public Ollama)

Optional secrets:
- `SLACK_WEBHOOK`: For notifications
- `JIRA_API_TOKEN`: For test case integration

## Jenkins

### Setup

1. Install required Jenkins plugins:
   - Pipeline Plugin
   - HTML Publisher Plugin
   - JUnit Plugin

2. Create new Pipeline job

3. Configure Pipeline from SCM:
   - Repository URL: Your repo
   - Script Path: `Jenkinsfile`

### Usage

**With parameters**:
```groovy
BRD_FILE: data/brd_sample.txt
TEST_NAME: MyTest
USE_STRONG_MODEL: true
```

**From CLI**:
```bash
curl -X POST "http://jenkins:8080/job/test-generation/buildWithParameters" \
  --user admin:token \
  --data "BRD_FILE=data/brd_sample.txt&TEST_NAME=MyTest"
```

## Docker

### Build Image

```bash
docker build -t ai-test-automation .
```

### Run Web Server

```bash
docker run -p 8000:8000 -p 11434:11434 ai-test-automation
```

### Generate Tests

```bash
docker run -v $(pwd)/data:/app/data \
           -v $(pwd)/outputs:/app/outputs \
           ai-test-automation generate \
           --brd /app/data/brd_sample.txt \
           --base-name MyTest
```

### Compile and Run

```bash
docker run -v $(pwd)/outputs:/app/outputs \
           ai-test-automation compile MyTest
```

## Local Execution

### Prerequisites

- Python 3.12+
- Java 11+
- Maven 3.9+
- Ollama running locally

### Generate Tests

```bash
python main.py --brd data/brd_sample.txt --base-name MyTest --use-strong-model
```

### Compile and Run (Linux/Mac)

```bash
chmod +x cicd/run_generated_tests.sh
./cicd/run_generated_tests.sh MyTest
```

### Compile and Run (Windows)

```powershell
.\cicd\run_generated_tests.ps1 -TestName "MyTest"
```

### View Reports

Open `test-project/target/site/surefire-report.html` in browser.

## GitLab CI

Create `.gitlab-ci.yml`:

```yaml
stages:
  - generate
  - compile
  - test

variables:
  BRD_FILE: "data/brd_sample.txt"
  TEST_NAME: "GeneratedTest"

generate_tests:
  stage: generate
  image: python:3.12
  before_script:
    - pip install -r requirements.txt
    - curl -fsSL https://ollama.com/install.sh | sh
    - ollama serve &
    - sleep 5
    - ollama pull qwen2.5:latest
  script:
    - python main.py --brd $BRD_FILE --base-name $TEST_NAME --use-strong-model
  artifacts:
    paths:
      - outputs/
    expire_in: 1 week

compile_tests:
  stage: compile
  image: maven:3.9-eclipse-temurin-11
  dependencies:
    - generate_tests
  script:
    - mkdir -p test-project/src/test/java/com/automation
    - cp outputs/tests/*.java test-project/src/test/java/com/automation/
    - cp cicd/pom.xml test-project/
    - cd test-project
    - mvn clean compile test-compile
  artifacts:
    paths:
      - test-project/target/
    expire_in: 1 day

run_tests:
  stage: test
  image: maven:3.9-eclipse-temurin-11
  dependencies:
    - compile_tests
  before_script:
    - apt-get update && apt-get install -y chromium chromium-driver
  script:
    - cd test-project
    - mvn test || true
    - mvn surefire-report:report
  artifacts:
    reports:
      junit: test-project/target/surefire-reports/*.xml
    paths:
      - test-project/target/site/
```

## Azure DevOps

Create `azure-pipelines.yml`:

```yaml
trigger:
  branches:
    include:
      - main
      - develop
  paths:
    include:
      - data/*
      - ai_automation/*

pool:
  vmImage: 'ubuntu-latest'

variables:
  BRD_FILE: 'data/brd_sample.txt'
  TEST_NAME: 'GeneratedTest'

stages:
  - stage: Generate
    jobs:
      - job: GenerateTests
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '3.12'
          
          - script: |
              pip install -r requirements.txt
            displayName: 'Install Python dependencies'
          
          - script: |
              curl -fsSL https://ollama.com/install.sh | sh
              ollama serve &
              sleep 5
              ollama pull qwen2.5:latest
            displayName: 'Setup Ollama'
          
          - script: |
              python main.py --brd $(BRD_FILE) --base-name $(TEST_NAME) --use-strong-model
            displayName: 'Generate tests'
          
          - publish: outputs/
            artifact: generated-tests

  - stage: Compile
    dependsOn: Generate
    jobs:
      - job: CompileTests
        steps:
          - task: JavaToolInstaller@0
            inputs:
              versionSpec: '11'
              jdkArchitectureOption: 'x64'
              jdkSourceOption: 'PreInstalled'
          
          - download: current
            artifact: generated-tests
          
          - script: |
              mkdir -p test-project/src/test/java/com/automation
              cp $(Pipeline.Workspace)/generated-tests/tests/*.java test-project/src/test/java/com/automation/
              cp cicd/pom.xml test-project/
            displayName: 'Setup project'
          
          - task: Maven@3
            inputs:
              mavenPomFile: 'test-project/pom.xml'
              goals: 'clean compile test-compile'
            displayName: 'Compile tests'

  - stage: Test
    dependsOn: Compile
    jobs:
      - job: RunTests
        steps:
          - task: Maven@3
            inputs:
              mavenPomFile: 'test-project/pom.xml'
              goals: 'test'
              testResultsFiles: '**/surefire-reports/*.xml'
            displayName: 'Run tests'
            continueOnError: true
          
          - task: PublishTestResults@2
            inputs:
              testResultsFormat: 'JUnit'
              testResultsFiles: 'test-project/target/surefire-reports/*.xml'
            displayName: 'Publish test results'
```

## Advanced Configuration

### Parallel Test Execution

Modify `pom.xml`:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <configuration>
        <parallel>methods</parallel>
        <threadCount>4</threadCount>
    </configuration>
</plugin>
```

### Custom Test Reports

Use Allure for better reports:

```xml
<dependency>
    <groupId>io.qameta.allure</groupId>
    <artifactId>allure-junit5</artifactId>
    <version>2.24.0</version>
</dependency>
```

### Selenium Grid Integration

Configure tests to use remote WebDriver:

```java
WebDriver driver = new RemoteWebDriver(
    new URL("http://selenium-hub:4444/wd/hub"),
    new ChromeOptions()
);
```

## Troubleshooting

### Compilation Fails

**Issue**: Generated Java code doesn't compile

**Solutions**:
1. Check Java version compatibility
2. Verify all dependencies in pom.xml
3. Review generated code for syntax errors
4. Enable detailed Maven output: `mvn -X compile`

### Tests Fail to Run

**Issue**: Selenium tests fail during execution

**Solutions**:
1. Ensure ChromeDriver is installed and in PATH
2. Run tests in headless mode: `-Dheadless=true`
3. Check browser compatibility
4. Verify test data and selectors

### Ollama Connection Issues

**Issue**: Cannot connect to Ollama service

**Solutions**:
1. Check Ollama is running: `ollama list`
2. Verify port 11434 is accessible
3. Pull model manually: `ollama pull qwen2.5:latest`
4. Check firewall settings

## Best Practices

1. **Version Control**: Commit generated tests to separate branch for review
2. **Test Data**: Use environment-specific test data
3. **Reporting**: Configure notifications for test failures
4. **Artifacts**: Archive generated code and reports
5. **Scheduling**: Run generation on schedule for regression suites
6. **Quality Gates**: Set pass/fail thresholds for test execution

## Next Steps

- Add test case management integration (TestRail, Zephyr)
- Implement test parallelization
- Configure cross-browser testing
- Set up monitoring and alerting
- Integrate with defect tracking systems
