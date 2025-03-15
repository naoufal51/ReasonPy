"""Python execution agent using LangGraph's ReAct pattern with E2B Code Interpreter."""

from langchain_core.tools import tool, Tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from e2b_code_interpreter import Sandbox
from langgraph.checkpoint.memory import MemorySaver
import os
import dotenv
import json
import atexit
from typing import Any, Optional

# Load environment variables
dotenv.load_dotenv()


class E2BCodeInterpreter:
    """
    Class that manages a persistent E2B sandbox for Python code execution.
    Handles creating the sandbox, executing code, and cleaning up resources.
    """
    
    def __init__(self):
        """Initialize the code interpreter with an E2B sandbox."""
        # Get E2B API key from environment
        self.api_key = os.getenv("E2B_API_KEY")
        if not self.api_key:
            print("WARNING: E2B_API_KEY environment variable not found. E2B sandbox will not work.")
            print("Please sign up at https://e2b.dev and set your API key.")
            self.sandbox = None
        else:
            try:
                self.sandbox = Sandbox(api_key=self.api_key)
                print("Created E2B sandbox")
                # Register cleanup on program exit
                atexit.register(self.close)
            except Exception as e:
                print(f"Error creating E2B sandbox: {e}")
                self.sandbox = None
    
    def execute_code(self, code: str, package_name: Optional[str] = None) -> dict:
        """
        Execute Python code in the sandbox, optionally installing packages first.
        
        Args:
            code: The Python code to execute
            package_name: Optional package(s) to install before execution
            
        Returns:
            Dictionary containing execution results, stdout, stderr, and any errors
        """
        if not self.sandbox:
            return {
                "error": "E2B sandbox not initialized. Check your API key.",
                "stdout": "",
                "stderr": "",
                "success": False
            }
        
        try:
            # Install package if specified
            install_output = ""
            if package_name and package_name.lower() != "none":
                install_result = self.sandbox.commands.run(f"pip install {package_name}")
                install_output = install_result.stdout

            # Execute the code
            execution = self.sandbox.run_code(code)
            
            # Return structured output
            return {
                "stdout": execution.text,
                "install_output": install_output if package_name and package_name.lower() != "none" else "",
                "error": execution.error if execution.error else "",
                "success": not execution.error
            }
        except Exception as e:
            return {
                "error": str(e),
                "stdout": "",
                "stderr": str(e),
                "success": False
            }
    
    def close(self):
        """Close the sandbox and clean up resources."""
        if self.sandbox:
            try:
                self.sandbox.close()
                print("Closed E2B sandbox")
            except Exception as e:
                print(f"Error closing E2B sandbox: {e}")


# Create a singleton instance of the code interpreter
code_interpreter = E2BCodeInterpreter()


@tool
def install_and_run_python(package_name: str, code: str) -> str:
    """
    Install a package (if needed) and run Python code in a sandbox.
    
    Args:
        package_name: Name of the package to install. Use "none" if no package installation is needed.
        code: Python code to execute
    """
    result = code_interpreter.execute_code(code, package_name)
    
    # Format the output nicely for the agent
    output_parts = []
    
    # Add installation output if present
    if result.get("install_output"):
        output_parts.append(f"Package installation output:\n{result['install_output']}")
    
    # Add code execution output
    if result.get("stdout"):
        output_parts.append(f"Code execution output:\n{result['stdout']}")
    
    # Add error message if present
    if result.get("error"):
        output_parts.append(f"Error:\n{result['error']}")
    
    # Combine all parts with separators
    return "\n\n".join(output_parts)


@tool
def cleanup_sandbox() -> str:
    """
    Explicitly clean up and kill the E2B sandbox to release resources.
    Call this when you're done using the code interpreter to ensure proper cleanup.
    
    Returns:
        A confirmation message indicating the sandbox was closed
    """
    try:
        code_interpreter.close()
        return "E2B sandbox has been successfully cleaned up and resources released."
    except Exception as e:
        return f"Error during sandbox cleanup: {str(e)}"


# Initialize search tool
tavily_tool = TavilySearchResults(max_results=2)

# System message for the agent
SYSTEM_MESSAGE = """You are a helpful AI assistant that can execute Python code in a secure sandbox environment.

IMPORTANT INSTRUCTIONS:

To execute Python code, ALWAYS use the install_and_run_python tool with these parameters:
1. package_name: Specify any package you need to install. Use "none" if no package installation is needed.
2. code: The Python code you want to execute.

Examples:
- If you need to run code with no package installation:
  install_and_run_python(package_name="none", code="print('Hello world')")
  
- If you need to install a package:
  install_and_run_python(package_name="pandas", code="import pandas as pd\ndf = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})\nprint(df)")
  
- If you need to install multiple packages:
  install_and_run_python(package_name="pandas matplotlib", code="import pandas as pd\nimport matplotlib.pyplot as plt\n...")

RESOURCE MANAGEMENT:
When you are finished with your code execution tasks, you SHOULD use the cleanup_sandbox tool to properly release resources by calling:
  cleanup_sandbox()
This ensures the E2B sandbox is properly terminated and helps prevent resource leaks.

IMPORTANT: For time-sensitive queries (like today's stock prices or current data):
- ALWAYS include datetime functionality in your code to get accurate current date and time
- Use `from datetime import datetime` and `datetime.now()` to get the current timestamp
- For time-zone aware operations, use `import pytz` and specify the appropriate timezone
- ALWAYS display the actual numerical values in your results, not just descriptions

Example for time-sensitive operations:
```python
from datetime import datetime, timedelta
import pytz

# Get current date and time
now = datetime.now()
print(f"Current date and time: {now}")

# Get current date in a specific timezone (like New York for stock market)
eastern = pytz.timezone('US/Eastern')
ny_time = datetime.now(eastern)
print(f"Current time in New York: {ny_time}")

# Get yesterday's date for historical comparison
yesterday = now - timedelta(days=1)
print(f"Yesterday's date: {yesterday.date()}")
```

Example for stock analysis with actual numerical display:
```python
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Get current date
today = datetime.now()
print(f"Current date: {today.strftime('%Y-%m-%d')}")

# Download NVIDIA stock data
ticker = "NVDA"
end_date = today.strftime('%Y-%m-%d')
start_date = (today - timedelta(days=100)).strftime('%Y-%m-%d')
data = yf.download(ticker, start=start_date, end=end_date)

# Calculate moving averages
data['SMA_20'] = data['Close'].rolling(window=20).mean()
data['SMA_50'] = data['Close'].rolling(window=50).mean()

# Display the last 5 rows with actual values
print(f"Latest {ticker} stock data with moving averages:")
print(data[['Close', 'SMA_20', 'SMA_50']].tail(5))

# Display current values
latest = data.iloc[-1]
print(f"\nLatest values for {ticker} ({data.index[-1].strftime('%Y-%m-%d')}):")
print(f"Close Price: ${latest['Close']:.2f}")
print(f"20-day SMA: ${latest['SMA_20']:.2f}")
print(f"50-day SMA: ${latest['SMA_50']:.2f}")
```

Unlike traditional Jupyter notebooks, the sandbox environment maintains state between executions. Variables and packages defined in previous executions will be available in future executions.

When writing Python code:
1. Include meaningful comments
2. Use print() statements to show results
3. Write clear, readable code
4. Handle potential errors when appropriate
5. ALWAYS display actual numerical values in results, not just descriptions

For data science tasks, you might need to install these packages:
- yfinance: For financial data (stocks, etc.)
- pandas: For data manipulation
- numpy: For numerical operations 
- matplotlib or seaborn: For visualizations
- plotly: For interactive visualizations
- scikit-learn: For machine learning
- pytz: For timezone handling
- datetime: Built-in module for date and time operations

For web requests, consider using the requests package.
"""

# Create a model and graph
model = ChatOpenAI(model="gpt-4o-mini", temperature=0, streaming=False)
# model = ChatOpenAI(model="o3-mini")

# Create a memory saver for the agent
memory = MemorySaver()

# Create the agent with proper configuration
e2b_graph = create_react_agent(
    model, 
    tools=[install_and_run_python, cleanup_sandbox, tavily_tool],
    prompt=SYSTEM_MESSAGE,
    checkpointer=memory,
    # interrupt_before=["tools"],
    # streaming=False  # Ensure responses are fully loaded, not streamed
) 