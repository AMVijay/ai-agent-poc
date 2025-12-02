"""LangChain agent for weather checking."""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from weather_tool import get_weather

# Load environment variables
load_dotenv()


def create_weather_agent():
    """Create and return a weather checking agent."""
    
    # Check for GitHub token first (for Codespaces)
    github_token = os.getenv("GITHUB_TOKEN")
    api_key = os.getenv("OPENAI_API_KEY")
    
    if github_token:
        # Use GitHub Models API (available in Codespaces)
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            base_url="https://models.inference.ai.azure.com",
            api_key=github_token
        )
        print("✓ Using GitHub Models API")
    elif api_key and api_key != "your-api-key-here":
        # Fall back to OpenAI
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_key=api_key
        )
        print("✓ Using OpenAI API")
    else:
        raise ValueError("No API key found. Set GITHUB_TOKEN (for Codespaces) or OPENAI_API_KEY in environment variables.")
    
    llm.temperature = 0
    
    # Define the weather tool using decorator
    @tool
    def weather_tool(city: str) -> str:
        """Get current weather information for a US city only. Input should be a US city name."""
        return get_weather(city)
    
    # Create tool list
    tools = [weather_tool]
    
    # Create the agent using LangGraph
    agent = create_react_agent(llm, tools)
    
    return agent


def main():
    """Main function to run the weather agent."""
    print("🌤️  Weather Agent initialized!")
    print("=" * 50)
    
    # Create the agent
    agent = create_weather_agent()
    
    # Example queries
    queries = [
        "What's the weather like in New York?",
        "Tell me about the weather in Los Angeles",
        "How's the weather in Chicago today?",
    ]
    
    for query in queries:
        print(f"\nUser: {query}")
        print("-" * 50)
        try:
            response = agent.invoke({"messages": [{"role": "user", "content": query}]})
            if "messages" in response:
                last_message = response["messages"][-1]
                if hasattr(last_message, 'content'):
                    print(f"Agent: {last_message.content}")
                else:
                    print(f"Agent: {str(last_message)}")
        except Exception as e:
            print(f"Error: {str(e)}")
        print("-" * 50)


if __name__ == "__main__":
    main()
