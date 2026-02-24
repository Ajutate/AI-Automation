"""LangGraph workflow for orchestrating Feature and Selenium agents with tool-based validation.

This workflow uses LangChain's official create_agent to create proper agents,
then orchestrates them in a StateGraph workflow with ACTUAL code validation using executable tools.
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from .agents import create_feature_agent, create_selenium_agent
from .tools import compile_java_code, validate_feature_syntax, check_java_dependencies, analyze_code_quality


class AgentState(TypedDict):
    """State shared across agents in the workflow."""
    brd_text: str
    feature_file: str
    step_definitions: str  # Cucumber step definitions
    runner_class: str  # Cucumber test runner
    selenium_test: str  # Legacy field for compatibility
    current_step: str
    messages: Annotated[list, add_messages]
    validation_results: dict  # Store validation results


class AutomationWorkflow:
    """Production workflow with tool-enabled validation.
    
    This workflow uses a validation agent that can actually execute tools to:
    - Compile Java code with javac
    - Validate Gherkin syntax
    - Check dependencies
    - Analyze code quality
    
    This makes it a truly autonomous system that validates its own outputs.
    """
    
    def __init__(self, use_strong_model: bool = True):
        # Create generation agents
        self.feature_agent, self.feature_model = create_feature_agent(use_strong_model=use_strong_model)
        self.selenium_agent, self.selenium_model = create_selenium_agent(use_strong_model=use_strong_model)
        
        self.workflow = self._build_workflow()
    
    def _generate_feature_node(self, state: AgentState) -> AgentState:
        """Node: Generate feature file from BRD."""
        print("\n🤖 Feature Agent: Generating feature file...")
        
        result = self.feature_agent.invoke({"messages": [{"role": "user", "content": state['brd_text']}]})
        if result.get('messages'):
            feature_file = result['messages'][-1].content
        else:
            feature_file = str(result)
        feature_file = feature_file.replace('```gherkin', '').replace('```', '').strip()
        
        return {**state, "feature_file": feature_file, "current_step": "feature_generated"}
    
    def _validate_feature_node(self, state: AgentState) -> AgentState:
        """Node: Validate feature file using direct tool calls."""
        print("\n🔧 Validating feature file...")
        
        # Call tools directly - NO AGENT LOOP
        syntax_result = validate_feature_syntax.invoke({"feature_content": state['feature_file']})
        quality_result = analyze_code_quality.invoke({"code": state['feature_file']})
        
        # Format validation report
        validation_report = f"""Feature Validation Results:
✓ Syntax Check: {syntax_result.get('status', 'unknown')}
  - {syntax_result.get('message', 'No message')}
✓ Quality Analysis:
  - Lines: {quality_result.get('lines', 0)}
  - Scenarios: {quality_result.get('methods', 0)}
"""
        
        print(f"   {syntax_result.get('message', '')}")
        
        return {
            **state,
            "validation_results": {"feature": validation_report},
            "current_step": "feature_validated"
        }
    
    def _generate_selenium_node(self, state: AgentState) -> AgentState:
        """Node: Generate Cucumber step definitions and runner."""
        print("\n🤖 Selenium Agent: Generating Cucumber step definitions...")
        
        result = self.selenium_agent.invoke({"messages": [{"role": "user", "content": state['feature_file']}]})
        if result.get('messages'):
            step_definitions = result['messages'][-1].content
        else:
            step_definitions = str(result)
        step_definitions = step_definitions.replace('```java', '').replace('```', '').strip()
        
        # Generate Cucumber runner class
        runner_class = self._generate_cucumber_runner(state['feature_file'])
        
        return {
            **state,
            "step_definitions": step_definitions,
            "runner_class": runner_class,
            "selenium_test": step_definitions,  # For backward compatibility
            "current_step": "selenium_generated"
        }
    
    def _validate_selenium_node(self, state: AgentState) -> AgentState:
        """Node: Validate and compile Java test using direct tool calls."""
        print("\n🔧 Validating Java code...")
        
        # Extract class name from Java code
        import re
        class_match = re.search(r'class\s+(\w+)', state['selenium_test'])
        class_name = class_match.group(1) if class_match else "GeneratedTest"
        
        # Call tools directly - NO AGENT LOOP
        deps_result = check_java_dependencies.invoke({"java_code": state['selenium_test']})
        compile_result = compile_java_code.invoke({"java_code": state['selenium_test'], "class_name": class_name})
        quality_result = analyze_code_quality.invoke({"code": state['selenium_test']})
        
        # Format validation report
        validation_report = f"""Java Validation Results:
✓ Dependencies: {deps_result.get('status', 'unknown')}
  - Missing: {len(deps_result.get('missing_dependencies', []))} imports
✓ Compilation: {compile_result.get('status', 'unknown')}
  - {compile_result.get('message', 'No message')}
✓ Quality:
  - Lines: {quality_result.get('lines', 0)}
  - Methods: {quality_result.get('methods', 0)}
"""
        
        print(f"   {compile_result.get('message', '')}")
        
        validation_dict = state.get("validation_results", {})
        validation_dict["selenium"] = validation_report
        
        return {
            **state,
            "validation_results": validation_dict,
            "current_step": "selenium_validated"
        }
    
    def _generate_cucumber_runner(self, feature_content: str) -> str:
        """Generate a Cucumber test runner class.
        
        Args:
            feature_content: Gherkin feature file content
            
        Returns:
            Complete Cucumber runner Java class code
        """
        # Extract feature name from first line
        feature_name = "Test"
        for line in feature_content.split('\n'):
            if line.strip().startswith('Feature:'):
                # Extract feature name and convert to PascalCase
                name = line.replace('Feature:', '').strip()
                # Simple conversion: remove special chars and capitalize words
                feature_name = ''.join(word.capitalize() for word in name.replace('-', ' ').replace('_', ' ').split())
                break
        
        runner_template = f'''import org.junit.runner.RunWith;
import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;

/**
 * Cucumber Test Runner
 * Binds feature files to step definitions for BDD execution
 */
@RunWith(Cucumber.class)
@CucumberOptions(
    features = "src/test/resources/features",
    glue = {{"stepdefinitions"}},
    plugin = {{
        "pretty",
        "html:target/cucumber-reports/cucumber.html",
        "json:target/cucumber-reports/cucumber.json",
        "junit:target/cucumber-reports/cucumber.xml"
    }},
    monochrome = true,
    dryRun = false
)
public class {feature_name}Runner {{
    // This class should remain empty
    // All test logic is in step definitions
}}
'''
        return runner_template
    
    def _build_workflow(self) -> StateGraph:
        """Build workflow with tool-enabled validation."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("generate_feature", self._generate_feature_node)
        workflow.add_node("validate_feature", self._validate_feature_node)
        workflow.add_node("generate_selenium", self._generate_selenium_node)
        workflow.add_node("validate_selenium", self._validate_selenium_node)
        
        # Define edges
        workflow.set_entry_point("generate_feature")
        workflow.add_edge("generate_feature", "validate_feature")
        workflow.add_edge("validate_feature", "generate_selenium")
        workflow.add_edge("generate_selenium", "validate_selenium")
        workflow.add_edge("validate_selenium", END)
        
        return workflow.compile()
    
    def execute(self, brd_text: str) -> dict:
        """Execute the tool-enabled validation workflow."""
        print("\n🚀 Starting Agentic Automation Workflow with Tool Validation...")
        print("=" * 60)
        print("✨ Using TOOLS to validate: compile Java, check syntax, analyze quality")
        print("=" * 60)
        
        initial_state: AgentState = {
            "brd_text": brd_text,
            "feature_file": "",
            "step_definitions": "",
            "runner_class": "",
            "selenium_test": "",
            "current_step": "start",
            "messages": [],
            "validation_results": {}
        }
        
        final_state = self.workflow.invoke(initial_state)
        
        print("\n✅ Workflow completed with validation!")
        print("=" * 60)
        
        # Print validation summary
        if final_state.get("validation_results"):
            print("\n📊 Validation Summary:")
            print("=" * 60)
            for key, value in final_state["validation_results"].items():
                print(f"\n{key.upper()}:")
                print(value[:300] + "..." if len(str(value)) > 300 else value)
        
        return {
            "feature_file": final_state["feature_file"],
            "step_definitions": final_state.get("step_definitions", final_state.get("selenium_test", "")),
            "runner_class": final_state.get("runner_class", ""),
            "selenium_test": final_state.get("selenium_test", ""),  # For backward compatibility
            "validation_results": final_state.get("validation_results", {})
        }
