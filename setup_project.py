"""Setup Maven project and resolve dependencies.

This script automates the complete project setup:
- Creates Maven project structure
- Copies generated tests and features
- Resolves all dependencies
- Compiles tests
- Configures VS Code

Usage:
    python setup_project.py
"""

from ai_automation.maven_setup import setup_maven_project

if __name__ == "__main__":
    setup_maven_project()
