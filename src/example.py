"""
Example script showing how to use the ReasonPy agent.

This demonstrates basic usage patterns for interacting with the
Python execution agent through natural language.
"""

import os
from dotenv import load_dotenv
from src.agent.graph import graph as local_graph
try:
    from src.agent.e2b_graph import graph as e2b_graph
    E2B_AVAILABLE = True
except ImportError:
    E2B_AVAILABLE = False

# Load environment variables from .env file if it exists
load_dotenv()

# Check for required API keys
if not os.getenv("OPENAI_API_KEY"):
    print("Warning: OPENAI_API_KEY not found in environment variables.")
    print("Set this key before running the agent.")

if not os.getenv("TAVILY_API_KEY"):
    print("Warning: TAVILY_API_KEY not found in environment variables.")
    print("Web search functionality will not work without this key.")

if not os.getenv("E2B_API_KEY") and E2B_AVAILABLE:
    print("Warning: E2B_API_KEY not found in environment variables.")
    print("E2B sandbox functionality will not work without this key.")
    print("Sign up at https://e2b.dev to get your API key.")

def run_agent_with_query(query, use_e2b=False):
    """Run the ReasonPy agent with a natural language query.
    
    Args:
        query (str): The natural language query to send to the agent
        use_e2b (bool): Whether to use the E2B sandbox environment
        
    Returns:
        The response from the agent
    """
    print(f"📝 Query: {query}\n")
    print("🔄 Thinking...\n")
    
    # Choose which execution environment to use
    if use_e2b and E2B_AVAILABLE:
        print("Using E2B sandbox environment")
        response = e2b_graph.invoke({"input": query})
    else:
        print("Using local Python REPL environment")
        response = local_graph.invoke({"input": query})
    
    print("\n✅ Response received!")
    return response

if __name__ == "__main__":
    # Example queries to demonstrate agent capabilities
    local_examples = [
        "Calculate the first 10 Fibonacci numbers",
        "Create a simple bar chart showing the months of the year and a random value for each",
        # Uncomment the line below to use web search (requires Tavily API key)
        # "Find and plot the population of the top 5 most populous countries"
    ]
    
    e2b_examples = [
        "Install pandas and calculate basic statistics on a sample dataset",
        "Install yfinance and get the last 7 days of Apple stock prices",
        "Install matplotlib, numpy and create a sine wave visualization"
    ] if E2B_AVAILABLE else []
    
    print("🤖 ReasonPy Agent Example\n")
    print("Select an execution environment:")
    print("1. Local Python REPL")
    if E2B_AVAILABLE:
        print("2. E2B Sandbox")
    
    env_choice = input("\nSelect environment (number): ")
    use_e2b = env_choice == "2" and E2B_AVAILABLE
    
    if use_e2b and E2B_AVAILABLE:
        print("\nE2B Sandbox Examples:")
        example_queries = e2b_examples
    else:
        print("\nLocal REPL Examples:")
        example_queries = local_examples
    
    print("Select a query to run or enter your own:")
    for i, query in enumerate(example_queries):
        print(f"{i+1}. {query}")
    print(f"{len(example_queries)+1}. Enter your own query")
    
    choice = input("\nEnter your choice (number): ")
    
    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(example_queries):
            query = example_queries[choice_num-1]
        else:
            query = input("\nEnter your query: ")
            
        # Run the agent with the selected/entered query
        result = run_agent_with_query(query, use_e2b=use_e2b)
        
        # Display the full result or just the final output based on preference
        print("\n📊 Final Output:")
        print(result["output"])
        
    except ValueError:
        print("Invalid choice. Please enter a number.")
    except Exception as e:
        print(f"An error occurred: {str(e)}") 