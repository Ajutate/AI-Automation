"""Tools for agent-based code validation and execution.

These tools enable agents to compile and run generated Java code.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Optional
from langchain_core.tools import tool


@tool
def compile_java_code(java_code: str, class_name: str) -> Dict[str, any]:
    """Compile Java code to validate syntax and structure.
    
    Args:
        java_code: The Java source code to compile
        class_name: Name of the Java class (without .java extension)
        
    Returns:
        Dict with status, message, and compilation details
    """
    try:
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write Java file
            java_file = Path(temp_dir) / f"{class_name}.java"
            java_file.write_text(java_code, encoding='utf-8')
            
            # Compile
            result = subprocess.run(
                ['javac', str(java_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Check if .class file was created
                class_file = Path(temp_dir) / f"{class_name}.class"
                if class_file.exists():
                    return {
                        "status": "success",
                        "message": f"✅ Compilation successful for {class_name}",
                        "compiled": True,
                        "errors": None,
                        "class_file_size": class_file.stat().st_size
                    }
                else:
                    return {
                        "status": "warning",
                        "message": "Compilation completed but .class file not found",
                        "compiled": False,
                        "errors": None
                    }
            else:
                return {
                    "status": "error",
                    "message": f"❌ Compilation failed",
                    "compiled": False,
                    "errors": result.stderr,
                    "stdout": result.stdout
                }
                
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": "Compilation timed out after 30 seconds",
            "compiled": False,
            "errors": "Timeout"
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "message": "Java compiler (javac) not found. Please install JDK.",
            "compiled": False,
            "errors": "javac not in PATH"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error during compilation: {str(e)}",
            "compiled": False,
            "errors": str(e)
        }


@tool
def validate_feature_syntax(feature_content: str) -> Dict[str, any]:
    """Validate Gherkin feature file syntax.
    
    Args:
        feature_content: The Gherkin feature file content
        
    Returns:
        Dict with validation status and details
    """
    required_keywords = ["Feature:", "Scenario:"]
    step_keywords = ["Given", "When", "Then", "And", "But"]
    
    issues = []
    warnings = []
    
    # Check for required keywords
    for keyword in required_keywords:
        if keyword not in feature_content:
            issues.append(f"Missing required keyword: {keyword}")
    
    # Check for at least one step
    has_steps = any(keyword in feature_content for keyword in step_keywords)
    if not has_steps:
        issues.append("No Gherkin steps found (Given/When/Then)")
    
    # Check for common issues
    lines = feature_content.split('\n')
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if line and not line.startswith('#'):
            # Check for steps without colons after Feature/Scenario keyword
            # Valid lines: "Feature: title", "Scenario: title", "Scenario Outline: title"
            # Invalid lines: "Feature title" or "Scenario title" (missing colon)
            if line.startswith('Feature') and not line.startswith('Feature:'):
                warnings.append(f"Line {i}: Missing colon after 'Feature'")
            elif line.startswith('Scenario') and not line.startswith(('Scenario:', 'Scenario Outline:', 'Scenario Template:')):
                warnings.append(f"Line {i}: Missing colon after 'Scenario'")
    
    # Determine status
    if issues:
        status = "invalid"
        message = f"❌ Feature file has {len(issues)} error(s)"
    elif warnings:
        status = "warning"
        message = f"⚠️ Feature file valid but has {len(warnings)} warning(s)"
    else:
        status = "valid"
        message = "✅ Feature file syntax is valid"
    
    return {
        "status": status,
        "message": message,
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "line_count": len(lines),
        "scenario_count": feature_content.count("Scenario:")
    }


@tool
def check_java_dependencies(java_code: str) -> Dict[str, any]:
    """Check if Java code uses proper dependencies and imports.
    
    Args:
        java_code: The Java source code to check
        
    Returns:
        Dict with dependency analysis
    """
    required_imports = {
        "JUnit 5": ["org.junit.jupiter", "@Test", "@BeforeEach", "@AfterEach"],
        "Selenium": ["org.openqa.selenium", "WebDriver"],
    }
    
    found_dependencies = []
    missing_dependencies = []
    
    for dep_name, patterns in required_imports.items():
        if any(pattern in java_code for pattern in patterns):
            found_dependencies.append(dep_name)
        else:
            missing_dependencies.append(dep_name)
    
    # Check for common best practices
    has_page_objects = "class" in java_code and "Page" in java_code
    has_assertions = any(word in java_code for word in ["assert", "Assert", "assertEquals"])
    has_setup = "@BeforeEach" in java_code or "setUp" in java_code
    has_teardown = "@AfterEach" in java_code or "tearDown" in java_code
    
    return {
        "status": "success",
        "message": f"Found {len(found_dependencies)} required dependencies",
        "found_dependencies": found_dependencies,
        "missing_dependencies": missing_dependencies,
        "best_practices": {
            "has_page_objects": has_page_objects,
            "has_assertions": has_assertions,
            "has_setup": has_setup,
            "has_teardown": has_teardown
        }
    }


@tool
def run_maven_test(test_class_name: str, project_dir: str = "test-project") -> Dict[str, any]:
    """Run Maven test for a specific test class.
    
    Args:
        test_class_name: Name of the test class to run
        project_dir: Directory containing the Maven project
        
    Returns:
        Dict with test execution results
    """
    try:
        # Check if Maven is available
        mvn_check = subprocess.run(['mvn', '--version'], capture_output=True, timeout=5)
        if mvn_check.returncode != 0:
            return {
                "status": "error",
                "message": "Maven not found. Please install Maven.",
                "executed": False
            }
        
        # Run Maven test
        result = subprocess.run(
            ['mvn', 'test', f'-Dtest={test_class_name}'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Parse output
        output = result.stdout + result.stderr
        
        tests_run = 0
        failures = 0
        errors = 0
        skipped = 0
        
        # Extract test statistics
        for line in output.split('\n'):
            if 'Tests run:' in line:
                parts = line.split(',')
                for part in parts:
                    if 'Tests run:' in part:
                        tests_run = int(part.split(':')[1].strip().split()[0])
                    elif 'Failures:' in part:
                        failures = int(part.split(':')[1].strip().split()[0])
                    elif 'Errors:' in part:
                        errors = int(part.split(':')[1].strip().split()[0])
                    elif 'Skipped:' in part:
                        skipped = int(part.split(':')[1].strip().split()[0])
        
        success = result.returncode == 0 and failures == 0 and errors == 0
        
        return {
            "status": "success" if success else "failure",
            "message": f"{'✅' if success else '❌'} Tests: {tests_run}, Failures: {failures}, Errors: {errors}",
            "executed": True,
            "tests_run": tests_run,
            "failures": failures,
            "errors": errors,
            "skipped": skipped,
            "success": success,
            "output_excerpt": output[-500:] if len(output) > 500 else output
        }
        
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": "Test execution timed out after 120 seconds",
            "executed": False
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "message": f"Project directory not found: {project_dir}",
            "executed": False
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error running tests: {str(e)}",
            "executed": False,
            "error_details": str(e)
        }


@tool
def analyze_code_quality(code: str, code_type: str = "java") -> Dict[str, any]:
    """Analyze code quality metrics.
    
    Args:
        code: Source code to analyze
        code_type: Type of code (java or gherkin)
        
    Returns:
        Dict with quality metrics
    """
    lines = code.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    comment_lines = [line for line in lines if line.strip().startswith(('//''/*', '*', '#'))]
    
    if code_type == "java":
        # Java-specific metrics
        class_count = code.count('class ')
        method_count = code.count('public ') + code.count('private ') + code.count('protected ')
        test_count = code.count('@Test')
        
        metrics = {
            "total_lines": len(lines),
            "code_lines": len(non_empty_lines),
            "comment_lines": len(comment_lines),
            "classes": class_count,
            "methods": method_count,
            "tests": test_count,
            "comment_ratio": len(comment_lines) / len(non_empty_lines) if non_empty_lines else 0
        }
    else:
        # Gherkin-specific metrics
        scenario_count = code.count('Scenario:')
        step_count = sum(1 for line in lines if any(line.strip().startswith(k) for k in ['Given', 'When', 'Then', 'And', 'But']))
        
        metrics = {
            "total_lines": len(lines),
            "scenarios": scenario_count,
            "steps": step_count,
            "avg_steps_per_scenario": step_count / scenario_count if scenario_count > 0 else 0
        }
    
    return {
        "status": "success",
        "message": "Code quality analysis completed",
        "metrics": metrics,
        "code_type": code_type
    }
