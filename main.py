"""CLI for BRD -> Feature -> Java test generation using LangGraph."""

import argparse
import logging
from pathlib import Path

from ai_automation.workflow import AutomationWorkflow
from ai_automation.generator import save_outputs
from ai_automation.logging_config import setup_logging


setup_logging()
logger = logging.getLogger(__name__)


def read_brd(path: str) -> str:
    """Read BRD file from path."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"BRD file not found: {file_path}")
    return file_path.read_text(encoding="utf-8")


def main() -> None:
    """Main entry point for workflow execution."""
    parser = argparse.ArgumentParser(
        description="BRD -> Feature -> Java test generator using LangGraph & LangChain"
    )
    parser.add_argument("--brd", required=True, help="Path to BRD text file")
    parser.add_argument("--base-name", default="GeneratedFeature", help="Base name for output files")
    parser.add_argument("--use-strong-model", action="store_true", help="Use stronger model for generation")
    parser.add_argument("--auto-setup-maven", action="store_true", 
                       help="Automatically setup Maven project and resolve dependencies after generation")
    args = parser.parse_args()
    logger.info("CLI generation started for BRD '%s' with base name '%s'", args.brd, args.base_name)

    # Read BRD
    print(f"\n📄 Reading BRD from: {args.brd}")
    brd_text = read_brd(args.brd)
    print(f"✓ BRD loaded ({len(brd_text)} characters)")

    # Execute workflow with tool validation
    workflow = AutomationWorkflow(
        use_strong_model=args.use_strong_model,
        auto_setup_maven=args.auto_setup_maven
    )
    results = workflow.execute(brd_text)

    # Save outputs
    print(f"\n💾 Saving generated files as '{args.base_name}'...")
    feature_path, step_def_path, runner_path = save_outputs(
        results["feature_file"],
        results.get("step_definitions", results.get("selenium_test", "")),
        args.base_name,
        results.get("runner_class", None)
    )

    # Display results
    print("\n" + "=" * 60)
    print("📦 Generated Files:")
    print(f"   • Feature: {feature_path}")
    print(f"   • Step Definitions: {step_def_path}")
    if runner_path:
        print(f"   • Test Runner: {runner_path}")
    print("=" * 60)
    print("\n✨ Generation complete!\n")
    logger.info("CLI generation finished for base name '%s'", args.base_name)


if __name__ == "__main__":
    main()
