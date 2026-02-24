"""Output file utilities for generated feature and test files."""

from pathlib import Path
from typing import Tuple

from .config import Config


def save_outputs(feature_text: str, java_text: str, base_name: str, runner_text: str = None) -> Tuple[str, str, str]:
    """Save feature file, step definitions, and optionally runner class.
    
    Args:
        feature_text: Gherkin feature file content
        java_text: Cucumber step definitions Java code
        base_name: Base name for output files
        runner_text: Optional Cucumber test runner class
        
    Returns:
        Tuple of (feature_path, step_definitions_path, runner_path)
    """
    cfg = Config()
    feature_dir = Path(cfg.output_feature_dir)
    test_dir = Path(cfg.output_test_dir)

    feature_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    # Save feature file
    feature_path = feature_dir / f"{base_name}.feature"
    feature_path.write_text(feature_text, encoding="utf-8")
    
    # Save step definitions
    step_def_path = test_dir / f"{base_name}StepDefinitions.java"
    step_def_path.write_text(java_text, encoding="utf-8")
    
    # Save runner class if provided
    runner_path = None
    if runner_text:
        runner_path = test_dir / f"{base_name}Runner.java"
        runner_path.write_text(runner_text, encoding="utf-8")

    return str(feature_path), str(step_def_path), str(runner_path) if runner_path else ""
