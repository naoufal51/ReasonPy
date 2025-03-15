# E2B Code Interpreter Agent

This implementation uses E2B's Code Interpreter to execute Python code in a secure, isolated sandbox environment. The sandbox persists across multiple executions, allowing functions, variables, and packages to be reused.

## Features

- Secure, isolated code execution in E2B's cloud sandbox
- Automatic package installation detection and handling
- Persistent sandbox that maintains state between code executions
- Package management with direct pip install commands
- Seamless integration with LangGraph's ReAct pattern

## Setup

### 1. Sign up for E2B

First, you need to sign up for an E2B account at [e2b.dev](https://e2b.dev/) and obtain an API key.

### 2. Set Environment Variables

Create a `.env` file in the project root with the following:

```
# E2B API Key
E2B_API_KEY=your_e2b_api_key_here

# OpenAI API Key (if using OpenAI models)
OPENAI_API_KEY=your_openai_api_key_here

# Tavily API Key (for web search functionality)
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. Install Dependencies

```bash
pip install dotenv e2b-code-interpreter langchain-openai langchain-core langgraph
```

## Usage

### Basic Usage

To use the E2B-powered agent:

```python
from agent.e2b_graph import e2b_graph

# Run the agent with a user query
result = e2b_graph.invoke({
    "messages": [("user", "Calculate the first 10 Fibonacci numbers")]
})

# Print the response
print(result["messages"][-1].content)
```

### Testing Persistence

You can run the included example to test persistence:

```bash
python src/e2b_persistent_example.py
```

This demonstrates how the sandbox maintains state between executions by:
1. Installing the emoji package and defining a function
2. Using that function in a subsequent query without reinstalling or redefining

## Adding More Packages

The implementation automatically detects and installs common packages like:
- numpy, pandas, matplotlib
- scikit-learn, tensorflow, torch
- nltk, beautifulsoup4, requests
- and many others

For other packages, you can use the `install_package` tool:

```
Use the install_package tool to install any additional package
```

## Technical Details

- The sandbox runs in E2B's secure cloud environment
- A single persistent sandbox is used for the entire session
- Packages are installed via pip using E2B's command execution
- The agent uses the LangGraph ReAct pattern for tool usage
- E2B provides better isolation and security than local Python REPL 