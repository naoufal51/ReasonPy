# ReasonPy: An Intelligent Python Execution Agent

ReasonPy is an AI-powered Python execution environment that combines the reasoning capabilities of large language models with a Python runtime. Built on LangGraph's ReAct pattern, it allows natural language interactions with a Python interpreter, enabling both code execution and web search capabilities.

## 🚀 Features

- **Python Code Execution**: Run Python code snippets directly from natural language prompts
- **Multiple Execution Environments**:
  - **Local Python REPL**: Execute code in a local Python environment
  - **E2B Sandbox**: Run code in a secure, isolated cloud sandbox with package installation capabilities
- **Web Search Integration**: Search the web for information using the Tavily API
- **Visualization Support**: Automatically saves matplotlib plots to the artifacts directory
- **LLM-Powered Reasoning**: Uses OpenAI models to understand requests and generate appropriate Python code
- **Error Handling**: Gracefully handles and reports errors in code execution
- **Package Management**: Install and use Python packages on-the-fly (E2B mode)

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Tavily API key (for web search functionality)
- E2B API key (for sandbox environment, sign up at https://e2b.dev)

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/naoufal51/ReasonPy.git
cd ReasonPy

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export OPENAI_API_KEY="your-openai-api-key"
export TAVILY_API_KEY="your-tavily-api-key"
export E2B_API_KEY="your-e2b-api-key"  # For E2B sandbox execution
```

## 📚 Usage

ReasonPy provides two distinct execution environments that can be used based on your needs:

### Local Python REPL

The default environment executes code locally in a Python REPL:

```python
from src.agent.graph import graph

# Example: Run the agent with a query using local Python REPL
response = graph.invoke({"input": "Create a bar chart showing the top 5 most populous countries"})
print(response)
```

### E2B Sandbox Environment

For more complex tasks that may require package installation or more secure execution:

```python
from src.agent.e2b_graph import graph as e2b_graph

# Example: Run the agent with a query using E2B sandbox
response = e2b_graph.invoke({"input": "Install pandas and plot stock prices for the last week"})
print(response)
```

The agent will:
1. Understand the request using an LLM
2. Generate appropriate Python code (including web searches if needed)
3. Execute the code in the selected environment and return the results
4. Save any visualizations to `./src/agent/artifacts/` (in local REPL mode)

## 🔄 Choosing the Right Environment

- **Local REPL (graph.py)**: Best for simple code execution and matplotlib visualizations
- **E2B Sandbox (e2b_graph.py)**: Best for:
  - Installing and using packages on-the-fly
  - Secure code execution in an isolated environment
  - Persistent state between executions
  - Resource-intensive operations

## 🏗️ Project Structure

```
ReasonPy/
├── src/
│   └── agent/
│       ├── artifacts/        # Directory for saved visualizations
│       ├── graph.py          # Local Python REPL implementation
│       └── e2b_graph.py      # E2B sandbox implementation
├── requirements.txt
└── README.md
```

## 🔮 Future Plans

This is an ongoing project with plans to add:

- Additional tool integrations
- Support for more complex Python workflows
- Persistent conversation history
- Fine-tuning capabilities
- Enhanced visualization options
- Custom agent configurations
- Multi-environment orchestration

### Advanced System Expansion

- **Multi-Agent System**: Implement a collaborative agent architecture where:
  - Multiple specialized agents work together on complex tasks
  - Agents with different capabilities (data retrieval, calculation, visualization) coordinate actions
  - Reasoning layers orchestrate workflow between agents
  - The system handles multi-step, complex workflows autonomously

- **Knowledge Management System**:
  - Process and index large amounts of private documents and code
  - Answer questions based on the organization's knowledge base
  - Generate reports and summaries from corporate data
  - Create and maintain documentation automatically

- **Continuous Learning System**:
  - Collect feedback from users to improve code generation
  - Build specialized knowledge for recurring tasks
  - Adapt to specific user preferences and coding styles
  - Continuously improve reasoning capabilities based on usage patterns

## 📄 License

[MIT License](LICENSE)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/naoufal51/ReasonPy/issues).

---

*Note: This project is under active development. Features and APIs may change as the project evolves.*