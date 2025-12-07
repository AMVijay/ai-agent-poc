"""LangChain agent for weather checking."""

import os
import re
import warnings
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from weather_tool import get_weather

# Suppress the deprecation warning from LangGraph
warnings.filterwarnings("ignore", message="create_react_agent has been moved")

# Load environment variables
load_dotenv()


def _is_weather_query(user_query: str) -> bool:
    """Internal helper to check if query is about weather in a US city."""
    user_lower = user_query.lower()
    weather_keywords = [
        'weather', 'temperature', 'temp', 'condition', 'humidity', 'wind',
        'rain', 'snow', 'sunny', 'cloudy', 'forecast', 'hot', 'cold'
    ]
    has_weather = any(kw in user_lower for kw in weather_keywords)
    has_city = bool(re.search(r'\b[A-Z][a-z]+\b', user_query))
    return has_weather and has_city


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
    
    # Define the validation tool
    @tool
    def validate_weather_query(user_query: str) -> str:
        """CRITICAL: Always call this tool first to validate if query is about weather in a US city.
        Returns 'valid' if query mentions weather keywords AND has a US city name, otherwise 'invalid'."""
        user_lower = user_query.lower()
        
        # Weather keywords
        weather_keywords = [
            'weather', 'temperature', 'temp', 'condition', 'humidity', 'wind',
            'rain', 'snow', 'sunny', 'cloudy', 'forecast', 'hot', 'cold'
        ]
        
        has_weather = any(kw in user_lower for kw in weather_keywords)
        has_city = bool(re.search(r'\b[A-Z][a-z]+\b', user_query))
        
        if not has_weather:
            return "invalid: Query doesn't mention weather"
        if not has_city:
            return "invalid: No US city mentioned in query"
        return "valid"
    
    # Define the weather tool using decorator
    @tool
    def weather_tool(city: str) -> str:
        """Get current weather information for a US city. Only use this after validate_weather_query returns 'valid'."""
        return get_weather(city)
    
    # Create tool list - validation tool first
    tools = [validate_weather_query, weather_tool]
    
    # Create the agent using create_react_agent from langgraph
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
        "2+2",  # This should be rejected
        "Tell me a joke",  # This should be rejected
    ]
    
    for query in queries:
        print(f"\nUser: {query}")
        print("-" * 50)
        
        # Client-side validation to enforce restriction
        if not _is_weather_query(query):
            print("Agent: I only answer questions about weather in US cities.")
            print("-" * 50)
            continue
        
        try:
            # Invoke the agent - validate_weather_query tool is available as a backup
            result = agent.invoke({"messages": [{"role": "user", "content": query}]})
            
            # Extract and display the output
            if "messages" in result:
                last_msg = result["messages"][-1]
                if hasattr(last_msg, 'content'):
                    print(f"Agent: {last_msg.content}")
                else:
                    print(f"Agent: {last_msg}")
            else:
                print(f"Agent: {result}")
        except Exception as e:
            print(f"Error: {str(e)}")
        print("-" * 50)
        print("-" * 50)


if __name__ == "__main__":
    main()

