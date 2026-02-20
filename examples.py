"""
Example usage of the AI Automation system.

This script demonstrates how to use the workflow programmatically.
"""

from ai_automation.workflow import AutomationWorkflow, ValidatedWorkflow
from ai_automation.generator import save_outputs


def example_basic_workflow():
    """Example: Basic workflow."""
    print("=" * 60)
    print("Example 1: Basic Workflow")
    print("=" * 60)
    
    # Sample BRD
    brd_text = """
    Business Requirement: User Registration
    
    The system shall allow new users to register an account.
    
    Requirements:
    1. User provides email, username, and password
    2. System validates email format
    3. System checks username uniqueness
    4. Password must be at least 8 characters
    5. Upon success, user receives confirmation email
    6. Upon failure, appropriate error message is shown
    """
    
    # Create and execute workflow
    workflow = AutomationWorkflow(use_strong_model=True)
    results = workflow.execute(brd_text)
    
    # Save results
    feature_path, java_path = save_outputs(
        results["feature_file"],
        results["selenium_test"],
        "UserRegistration"
    )
    
    print(f"\n✅ Files saved:")
    print(f"   Feature: {feature_path}")
    print(f"   Java: {java_path}")


def example_validated_workflow():
    """Example: Validated workflow with quality review steps."""
    print("\n" + "=" * 60)
    print("Example 2: Enhanced Workflow with Reviews")
    print("=" * 60)
    
    brd_text = """
    Business Requirement: Shopping Cart
    
    The system shall allow users to manage a shopping cart.
    
    Requirements:
    1. Add items to cart
    2. Update item quantities
    3. Remove items from cart
    4. View cart total
    5. Proceed to checkout
    6. Save cart for later
    """
    
    workflow = ValidatedWorkflow(use_strong_model=True)
    results = workflow.execute(brd_text)
    
    feature_path, java_path = save_outputs(
        results["feature_file"],
        results["selenium_test"],
        "ShoppingCart"
    )
    
    print(f"\n✅ Files saved:")
    print(f"   Feature: {feature_path}")
    print(f"   Java: {java_path}")


def example_custom_usage():
    """Example: Using agents individually."""
    print("\n" + "=" * 60)
    print("Example 3: Using Agents Individually")
    print("=" * 60)
    
    from ai_automation.agents import FeatureAgent, SeleniumAgent
    
    brd_text = """
    Business Requirement: Password Reset
    
    Users can reset their password using email verification.
    """
    
    # Use Feature Agent
    print("\n🤖 Running Feature Agent...")
    feature_agent = FeatureAgent(use_strong_model=True)
    feature = feature_agent.generate_feature(brd_text)
    print(f"✓ Feature generated ({len(feature)} characters)")
    
    # Use Selenium Agent
    print("\n🤖 Running Selenium Agent...")
    selenium_agent = SeleniumAgent(use_strong_model=True)
    java_test = selenium_agent.generate_selenium_test(feature)
    print(f"✓ Java test generated ({len(java_test)} characters)")
    
    # Save
    feature_path, java_path = save_outputs(feature, java_test, "PasswordReset")
    print(f"\n✅ Files saved:")
    print(f"   Feature: {feature_path}")
    print(f"   Java: {java_path}")


def example_workflow_state_inspection():
    """Example: Inspecting workflow state."""
    print("\n" + "=" * 60)
    print("Example 4: Workflow State Inspection")
    print("=" * 60)
    
    from ai_automation.workflow import AgentState
    
    brd_text = "User Login: Allow users to login with email and password."
    
    # Create workflow
    workflow = AutomationWorkflow(use_strong_model=False)
    
    # Initial state
    initial_state: AgentState = {
        "brd_text": brd_text,
        "feature_file": "",
        "selenium_test": "",
        "current_step": "start",
        "messages": []
    }
    
    print("\n📊 Initial State:")
    print(f"   BRD Length: {len(initial_state['brd_text'])} chars")
    print(f"   Current Step: {initial_state['current_step']}")
    
    # Execute
    final_state = workflow.workflow.invoke(initial_state)
    
    print("\n📊 Final State:")
    print(f"   Feature Length: {len(final_state['feature_file'])} chars")
    print(f"   Test Length: {len(final_state['selenium_test'])} chars")
    print(f"   Current Step: {final_state['current_step']}")
    print(f"   Messages: {len(final_state['messages'])}")


if __name__ == "__main__":
    print("\n🚀 Agentic AI Automation - Usage Examples\n")
    
    # Run examples
    try:
        example_basic_workflow()
        example_validated_workflow()
        example_custom_usage()
        example_workflow_state_inspection()
        
        print("\n" + "=" * 60)
        print("✨ All examples completed successfully!")
        print("=" * 60)
        print("\nCheck the outputs/ directory for generated files.\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. Ollama is running (http://localhost:11434)")
        print("  2. Models are pulled (ollama pull qwen2.5:latest)")
        print("  3. Dependencies are installed (pip install -r requirements.txt)")
