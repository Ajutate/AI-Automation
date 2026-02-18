"""CLI for BRD -> Feature -> Java test generation using LangGraph."""

import argparse
from pathlib import Path

from ai_automation.workflow import AutomationWorkflow, ParallelAgentWorkflow
from ai_automation.generator import save_outputs


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
    parser.add_argument(
        "--workflow",
        choices=["standard", "parallel"],
        default="standard",
        help="Workflow type: 'standard' for sequential agents, 'parallel' for enhanced workflow with review steps"
    )
    args = parser.parse_args()

    # Read BRD
    print(f"\n📄 Reading BRD from: {args.brd}")
    brd_text = read_brd(args.brd)
    print(f"✓ BRD loaded ({len(brd_text)} characters)")

    # Select and execute workflow
    if args.workflow == "parallel":
        workflow = ParallelAgentWorkflow(use_strong_model=args.use_strong_model)
    else:
        workflow = AutomationWorkflow(use_strong_model=args.use_strong_model)
    
    # Execute agentic workflow
    results = workflow.execute(brd_text)

    # Save outputs
    print(f"\n💾 Saving generated files as '{args.base_name}'...")
    feature_path, java_path = save_outputs(
        results["feature_file"],
        results["selenium_test"],
        args.base_name
    )

    # Display results
    print("\n" + "=" * 60)
    print("📦 Generated Files:")
    print(f"   • Feature: {feature_path}")
    print(f"   • Java Test: {java_path}")
    print("=" * 60)
    print("\n✨ Generation complete!\n")


if __name__ == "__main__":
    main()
