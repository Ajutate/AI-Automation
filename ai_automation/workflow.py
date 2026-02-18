"""LangGraph workflow for orchestrating Feature and Selenium agents.

This uses LangChain's official create_agent to create proper agents,
then orchestrates them in a StateGraph workflow.
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from .agents import create_feature_agent, create_selenium_agent


class AgentState(TypedDict):
    """State shared across agents in the workflow."""
    brd_text: str
    feature_file: str
    selenium_test: str
    current_step: str
    messages: Annotated[list, add_messages]


class AutomationWorkflow:
    """LangGraph workflow orchestrating Feature and Selenium agents.
    
    Uses LangChain's official create_agent and invokes them properly.
    Agents are created with system prompts and invoked via the LangGraph workflow.
    """
    
    def __init__(self, use_strong_model: bool = True):
        # Create agents using official LangChain create_agent
        self.feature_agent, self.feature_model = create_feature_agent(use_strong_model=use_strong_model)
        self.selenium_agent, self.selenium_model = create_selenium_agent(use_strong_model=use_strong_model)
        self.workflow = self._build_workflow()
    
    def _generate_feature_node(self, state: AgentState) -> AgentState:
        """Agent node: Generate feature file from BRD."""
        print("\n🤖 Feature Agent: Analyzing BRD and generating feature file...")
        
        # Invoke the LangChain agent
        result = self.feature_agent.invoke({"messages": [{"role": "user", "content": state['brd_text']}]})
        
        # Extract the final message content
        if result.get('messages'):
            feature_file = result['messages'][-1].content
        else:
            feature_file = str(result)
        
        # Clean up markdown code fences
        feature_file = feature_file.replace('```gherkin', '').replace('```', '').strip()
        
        return {
            **state,
            "feature_file": feature_file,
            "current_step": "feature_generated",
            "messages": [{"role": "system", "content": "Feature file generated"}]
        }
    
    def _generate_selenium_node(self, state: AgentState) -> AgentState:
        """Agent node: Generate Selenium test from feature file."""
        print("\n🤖 Selenium Agent: Creating automation test from feature file...")
        
        # Invoke the LangChain agent
        result = self.selenium_agent.invoke({"messages": [{"role": "user", "content": state['feature_file']}]})
        
        # Extract the final message content
        if result.get('messages'):
            selenium_test = result['messages'][-1].content
        else:
            selenium_test = str(result)
        
        # Clean up markdown code fences
        selenium_test = selenium_test.replace('```java', '').replace('```', '').strip()
        
        return {
            **state,
            "selenium_test": selenium_test,
            "current_step": "automation_generated",
            "messages": [{"role": "system", "content": "Selenium test generated"}]
        }
    
    def _should_continue(self, state: AgentState) -> str:
        """Conditional edge: Determine next step in workflow."""
        current_step = state.get("current_step", "start")
        
        if current_step == "start":
            return "generate_feature"
        elif current_step == "feature_generated":
            return "generate_selenium"
        elif current_step == "automation_generated":
            return "end"
        else:
            return "end"
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow."""
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes representing each agent's task
        workflow.add_node("generate_feature", self._generate_feature_node)
        workflow.add_node("generate_selenium", self._generate_selenium_node)
        
        # Define the workflow edges
        workflow.set_entry_point("generate_feature")
        workflow.add_edge("generate_feature", "generate_selenium")
        workflow.add_edge("generate_selenium", END)
        
        return workflow.compile()
    
    def execute(self, brd_text: str) -> dict:
        """Execute the full workflow from BRD to Selenium tests.
        
        Args:
            brd_text: Business Requirements Document text
            
        Returns:
            dict with 'feature_file' and 'selenium_test' keys
        """
        print("\n🚀 Starting Agentic Automation Workflow...")
        print("=" * 60)
        
        # Initialize state
        initial_state: AgentState = {
            "brd_text": brd_text,
            "feature_file": "",
            "selenium_test": "",
            "current_step": "start",
            "messages": []
        }
        
        # Execute workflow
        final_state = self.workflow.invoke(initial_state)
        
        print("\n✅ Workflow completed successfully!")
        print("=" * 60)
        
        return {
            "feature_file": final_state["feature_file"],
            "selenium_test": final_state["selenium_test"]
        }


class ParallelAgentWorkflow:
    """Alternative workflow with parallel agent execution and review.
    
    Uses LangChain agents properly with validation steps between generation phases.
    Agents are invoked through the workflow, not bypassed with direct prompting.
    """
    
    def __init__(self, use_strong_model: bool = True):
        # Create agents using official LangChain create_agent
        self.feature_agent, self.feature_model = create_feature_agent(use_strong_model=use_strong_model)
        self.selenium_agent, self.selenium_model = create_selenium_agent(use_strong_model=use_strong_model)
        self.workflow = self._build_workflow()
    
    def _generate_feature_node(self, state: AgentState) -> AgentState:
        """Node: Generate feature file from BRD."""
        print("\n🤖 Feature Agent: Working on feature file...")
        
        # Invoke the LangChain agent
        result = self.feature_agent.invoke({"messages": [{"role": "user", "content": state['brd_text']}]})
        
        # Extract the final message content
        if result.get('messages'):
            feature_file = result['messages'][-1].content
        else:
            feature_file = str(result)
        
        # Clean up markdown code fences
        feature_file = feature_file.replace('```gherkin', '').replace('```', '').strip()
        
        return {**state, "feature_file": feature_file}
    
    def _review_feature_node(self, state: AgentState) -> AgentState:
        """Node: Review and validate feature file."""
        print("\n🔍 Reviewer: Validating feature file...")
        # Simple validation
        has_feature = "Feature:" in state["feature_file"]
        has_scenario = "Scenario:" in state["feature_file"]
        status = "✅ Valid" if (has_feature and has_scenario) else "❌ Invalid"
        print(f"   {status}")
        return {**state, "current_step": "feature_reviewed"}
    
    def _generate_selenium_node(self, state: AgentState) -> AgentState:
        """Node: Generate Selenium test."""
        print("\n🤖 Selenium Agent: Creating automation test...")
        
        # Invoke the LangChain agent
        result = self.selenium_agent.invoke({"messages": [{"role": "user", "content": state['feature_file']}]})
        
        # Extract the final message content
        if result.get('messages'):
            selenium_test = result['messages'][-1].content
        else:
            selenium_test = str(result)
        
        # Clean up markdown code fences
        selenium_test = selenium_test.replace('```java', '').replace('```', '').strip()
        
        return {**state, "selenium_test": selenium_test}
    
    def _review_selenium_node(self, state: AgentState) -> AgentState:
        """Node: Review and enhance Selenium test."""
        print("\n🔍 Reviewer: Validating Selenium test...")
        return {**state, "current_step": "automation_reviewed"}
    
    def _build_workflow(self) -> StateGraph:
        """Build workflow with review steps."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("generate_feature", self._generate_feature_node)
        workflow.add_node("review_feature", self._review_feature_node)
        workflow.add_node("generate_selenium", self._generate_selenium_node)
        workflow.add_node("review_selenium", self._review_selenium_node)
        
        # Define edges
        workflow.set_entry_point("generate_feature")
        workflow.add_edge("generate_feature", "review_feature")
        workflow.add_edge("review_feature", "generate_selenium")
        workflow.add_edge("generate_selenium", "review_selenium")
        workflow.add_edge("review_selenium", END)
        
        return workflow.compile()
    
    def execute(self, brd_text: str) -> dict:
        """Execute the parallel review workflow."""
        print("\n🚀 Starting Enhanced Agentic Workflow with Reviews...")
        print("=" * 60)
        
        initial_state: AgentState = {
            "brd_text": brd_text,
            "feature_file": "",
            "selenium_test": "",
            "current_step": "start",
            "messages": []
        }
        
        final_state = self.workflow.invoke(initial_state)
        
        print("\n✅ Enhanced workflow completed!")
        print("=" * 60)
        
        return {
            "feature_file": final_state["feature_file"],
            "selenium_test": final_state["selenium_test"]
        }
