"""LangChain agent for weather checking."""

import os
import re
import warnings
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from weather_tool import get_weather

# Suppress the deprecation warning from LangGraph
warnings.filterwarnings("ignore", message="create_react_agent has been moved")

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
        # Check for capitalized word (city name) OR any word after "in"/"about"
        # More lenient: look for words after in/about, even with punctuation
        has_city = bool(re.search(r'\b[A-Z][a-z]*\b', user_query)) or bool(re.search(r'(?:in|about)\s+([a-z]+)', user_lower))
        
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
    
    # System prompt that enforces validation
    def make_prompt(state):
        """Create prompt with system message."""
        system_msg = SystemMessage(content="""You are a weather assistant. You MUST follow these rules:

1. ALWAYS call validate_weather_query tool FIRST for every user query
2. Only if validate_weather_query returns 'valid', then use weather_tool to get the weather
3. If validate_weather_query returns 'invalid', respond: "I only answer questions about weather in US cities. Please ask about the weather in a specific US city."
4. Do NOT answer any other questions - refuse politely and remind the user about the weather-only scope
5. Do NOT make assumptions or bypass the validation tool""")
        return [system_msg] + state["messages"]
    
    # Create tool list - validation tool first
    tools = [validate_weather_query, weather_tool]
    
    # Create the agent using create_react_agent from langgraph
    agent = create_react_agent(llm, tools, prompt=make_prompt)
    
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
        
        try:
            # Invoke the agent (validation is handled by the agent itself)
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

