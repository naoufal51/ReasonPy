"""Simple Python execution agent using LangGraph's ReAct pattern."""

from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
import os


# Create a Python REPL instance with matplotlib configuration
python_repl = PythonREPL()

# Configure matplotlib to use a non-interactive backend
setup_code = """
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend that doesn't require a GUI
import os

# Ensure artifacts directory exists
artifacts_dir = './src/agent/artifacts'
os.makedirs(artifacts_dir, exist_ok=True)
"""
python_repl.run(setup_code)

# Initialize search tool
tavily_tool = TavilySearchResults(max_results=2)


@tool
def run_python(code: str) -> str:
    """Execute Python code and return the result.
    
    Args:
        code: A string containing Python code to execute
    """
    try:
        # Create artifacts directory if it doesn't exist
        artifacts_dir = './src/agent/artifacts'
        os.makedirs(artifacts_dir, exist_ok=True)
        
        # Add figure saving code for matplotlib
        if "import matplotlib" in code or "import plt" in code or "from matplotlib" in code:
            plot_path = f"{artifacts_dir}/figure.png"
            if "plt.show()" in code:
                # Replace plt.show() with code to save and display the figure
                code = code.replace(
                    "plt.show()", 
                    f"plt.savefig('{plot_path}')\nprint('Figure saved to {plot_path}')"
                )
            elif "plt" in code and not "savefig" in code:
                # Add savefig if plt is used but no saving mechanism exists
                code += f"\nplt.savefig('{plot_path}')\nprint('Figure saved to {plot_path}')"
                
        result = python_repl.run(code)
        return result
    except Exception as e:
        return f"Error: {str(e)}"


# Simple system message for the agent
SYSTEM_MESSAGE = """You are a helpful AI assistant that can execute Python code.

When writing Python code:
1. Always include meaningful comments
2. Use print() statements to show results
3. Write clear, readable code
4. Handle potential errors when appropriate

When creating visualizations with matplotlib:
- Do NOT use plt.show() as it won't work in this environment
- The system will automatically save figures to the ./src/agent/artifacts directory
- Results will be displayed as text output

You have access to a Python execution environment via the run_python tool.
You can also search the web using the tavily_search_results tool.
"""

# Create a simple model and graph
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

graph = create_react_agent(
    model, 
    tools=[run_python, tavily_tool],
    prompt=SYSTEM_MESSAGE,
    checkpointer=memory,
    # interrupt_before=["tools"]
)
