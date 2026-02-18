"""Prompt templates for BRD -> Feature -> Java test generation."""

FEATURE_PROMPT = """You are a senior QA analyst. Convert the following BRD into a Gherkin feature file.

Requirements:
- Output only valid Gherkin (Feature, Background if needed, Scenarios)
- Use Given/When/Then/And steps
- Keep scenarios concise and testable
- Cover main flows and at least 1 negative/edge case
- Use business terminology from the BRD

BRD:
{brd}

Generate the feature file now:"""


JAVA_TEST_PROMPT = """You are a senior QA automation engineer. Generate Java Selenium test code from the Gherkin feature below.

Requirements:
- Use JUnit 5
- Use Selenium WebDriver
- Use Page Object pattern (create minimal Page Objects as inner classes or separate classes)
- Keep code compile-ready but minimal
- Add TODOs for selectors and test data
- Use clear method names aligned with steps

Gherkin Feature:
{feature}

Output only Java code:"""
