"""LangChain agent for weather checking."""

import os
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from weather_tool import get_weather

# Load environment variables
load_dotenv()


def is_weather_query(user_input: str) -> tuple[bool, str]:
    """
    Validate if the user input is a weather-related query about a city.
    Returns (is_valid, message)
    """
    user_lower = user_input.lower()
    
    # Keywords that indicate weather-related queries
    weather_keywords = [
        'weather', 'temperature', 'temp', 'cold', 'hot', 'humid', 'humidity',
        'wind', 'rain', 'snow', 'sunny', 'cloudy', 'forecast', 'condition',
        'climate', 'degrees', 'fahrenheit', 'celsius', 'precipitation',
        'how is it', "what's it like", 'how is the weather', 'tell me about'
    ]
    
    # Check if input contains weather keywords
    has_weather_keyword = any(keyword in user_lower for keyword in weather_keywords)
    
    # Check if input mentions a city (has proper nouns or city names)
    city_pattern = r'\b[A-Z][a-z]+\b|new york|los angeles|san francisco|san diego'
    has_city = bool(re.search(city_pattern, user_input))
    
    # Math/calculation detection
    math_pattern = r'^[0-9\s\+\-\*/\(\)]+$'
    is_math = bool(re.match(math_pattern, user_input.replace('?', '')))
    
    if is_math:
        return False, "I only answer weather-related questions. Please ask about the weather in a US city!"
    
    if not has_weather_keyword:
        return False, "I'm a weather assistant. Please ask about weather conditions in a US city."
    
    if not has_city:
        return False, "Please specify a US city in your query."
    
    return True, ""


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
        "2+2",  # This should be rejected
        "Tell me a joke",  # This should be rejected
    ]
    
    for query in queries:
        print(f"\nUser: {query}")
        print("-" * 50)
        
        # Validate if the query is weather-related about a city
        is_valid, error_message = is_weather_query(query)
        if not is_valid:
            print(f"Agent: {error_message}")
            print("-" * 50)
            continue
        
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
