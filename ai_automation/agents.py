"""Agent definitions using LangChain's official create_agent.

This module creates agents using langchain.agents.create_agent which is
the official, modern way to create tool-using agents in LangChain.
"""

from typing import Any, List
from langchain.agents import create_agent
from langchain_core.language_models.llms import LLM
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import tool
from pydantic import Field

from .ollama_client import generate_text
from .config import Config


class OllamaLLM(LLM):
    """Custom Ollama LLM wrapper for LangChain."""
    
    model_name: str = Field(default="qwen2.5:latest")
    temperature: float = Field(default=0.2)
    
    @property
    def _llm_type(self) -> str:
        return "ollama"
    
    def _call(self, prompt: str, stop: List[str] | None = None, **kwargs: Any) -> str:
        """Call Ollama API."""
        return generate_text(
            prompt=prompt,
            model=self.model_name,
            temperature=self.temperature
        )


class OllamaChatModel(BaseChatModel):
    """Chat model wrapper for Ollama (required for create_agent)."""
    
    model_name: str = Field(default="qwen2.5:latest")
    temperature: float = Field(default=0.2)
    bound_tools: List = Field(default_factory=list)
    
    @property
    def _llm_type(self) -> str:
        return "ollama-chat"
    
    def bind_tools(self, tools, **kwargs):
        """Bind tools to the model (required for create_agent)."""
        # Return a new instance with tools bound
        return self.__class__(
            model_name=self.model_name,
            temperature=self.temperature,
            bound_tools=list(tools)
        )
    
    def _generate(self, messages, stop=None, **kwargs):
        """Generate response from Ollama."""
        from langchain_core.messages import AIMessage, ToolCall
        from langchain_core.outputs import ChatGeneration, ChatResult
        import json
        import uuid
        
        # Convert messages to prompt
        prompt_parts = []
        for msg in messages:
            if hasattr(msg, 'content'):
                content = msg.content if isinstance(msg.content, str) else str(msg.content)
                prompt_parts.append(content)
        prompt = "\n".join(prompt_parts)
        
        # If tools are bound, add tool descriptions to prompt
        if self.bound_tools:
            tool_descriptions = "\n\nAvailable tools:\n"
            for tool in self.bound_tools:
                tool_name = tool.name if hasattr(tool, 'name') else str(tool)
                tool_desc = tool.description if hasattr(tool, 'description') else ""
                tool_descriptions += f"- {tool_name}: {tool_desc}\n"
            
            prompt = f"{prompt}\n{tool_descriptions}\n\nYou can use these tools by responding with: USE_TOOL: <tool_name> | <arguments>"
        
        # Call Ollama
        response = generate_text(prompt, model=self.model_name, temperature=self.temperature)
        
        # Check if response wants to use a tool
        if "USE_TOOL:" in response and self.bound_tools:
            # Parse tool call (simple format: USE_TOOL: tool_name | args)
            try:
                parts = response.split("USE_TOOL:")[1].strip().split("|")
                tool_name = parts[0].strip()
                tool_args = parts[1].strip() if len(parts) > 1 else ""
                
                # Create tool call message
                tool_call = ToolCall(
                    name=tool_name,
                    args={"input": tool_args},
                    id=f"call_{uuid.uuid4().hex[:8]}"
                )
                message = AIMessage(content="", tool_calls=[tool_call])
            except:
                # If parsing fails, return as regular message
                message = AIMessage(content=response)
        else:
            message = AIMessage(content=response)
        
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])


# Agent creation functions

def create_feature_agent(use_strong_model: bool = True):
    """Create a LangChain agent for feature file generation.
    
    Uses langchain.agents.create_agent without tools (Ollama doesn't support tool calling).
    Returns a compiled agent graph that can be invoked.
    """
    cfg = Config()
    model_name = cfg.strong_model if use_strong_model else cfg.primary_model
    
    # Create chat model for the agent
    llm = OllamaChatModel(model_name=model_name)
    
    # System prompt with instructions (no tools needed for Ollama)
    system_prompt = f"""You are a senior QA analyst specializing in BDD/Gherkin.
Your task is to create high-quality Gherkin feature files from Business Requirements Documents.

When given a BRD, analyze it and generate a complete Gherkin feature file with:
- Feature description
- Background (if needed)
- Multiple scenarios with Given/When/Then steps
- At least one negative test case
- Proper Gherkin syntax

Output ONLY the Gherkin feature file content, no explanations."""
    
    # Create agent without tools (Ollama doesn't support tool calling)
    agent = create_agent(
        model=llm,
        tools=None,
        system_prompt=system_prompt
    )
    
    return agent, model_name


def create_selenium_agent(use_strong_model: bool = True):
    """Create a LangChain agent for Selenium test generation.
    
    Uses langchain.agents.create_agent without tools (Ollama doesn't support tool calling).
    Returns a compiled agent graph that can be invoked.
    """
    cfg = Config()
    model_name = cfg.strong_model if use_strong_model else cfg.primary_model
    
    # Create chat model for the agent
    llm = OllamaChatModel(model_name=model_name)
    
    # System prompt with instructions
    system_prompt = """You are a senior QA automation engineer specializing in Selenium WebDriver and Java.
Your task is to create production-ready Selenium automation code from Gherkin feature files.

When given a Gherkin feature file, generate a complete Java test class with:
- JUnit 5 annotations (@Test, @BeforeEach, @AfterEach)
- WebDriver setup and teardown
- Page Object Model design
- Complete test methods with assertions
- Proper imports
- Clean, production-ready code

Output ONLY the Java code, no explanations."""
    
    # Create agent without tools (Ollama doesn't support tool calling)
    agent = create_agent(
        model=llm,
        tools=None,
        system_prompt=system_prompt
    )
    
    return agent, model_name
