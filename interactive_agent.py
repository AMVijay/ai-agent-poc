"""Interactive weather agent using LangGraph."""

import os
import sys
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
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
    # This is a simple heuristic - looks for capitalized words or common city patterns
    city_pattern = r'\b[A-Z][a-z]+\b|new york|los angeles|san francisco|san diego'
    has_city = bool(re.search(city_pattern, user_input))
    
    # Math/calculation detection
    math_pattern = r'^[0-9\s\+\-\*/\(\)]+$'
    is_math = bool(re.match(math_pattern, user_input.replace('?', '')))
    
    if is_math:
        return False, "❌ I only answer weather-related questions. Please ask about the weather in a US city!"
    
    if not has_weather_keyword:
        return False, "❌ I'm a weather assistant. Please ask about weather conditions in a US city (e.g., 'What's the weather in Boston?')"
    
    if not has_city:
        return False, "❌ Please specify a US city. For example: 'What's the weather in Miami?' or 'How's it in Seattle?'"
    
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
    """Main function for interactive weather agent."""
    try:
        print("🌤️  Welcome to Weather Agent!")
        print("=" * 60)
        print("Ask me about the weather in any US city.")
        print("Type 'quit' or 'exit' to leave.\n")
        
        # Create the agent
        agent = create_weather_agent()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit']:
                    print("\nGoodbye! 👋")
                    break
                
                # Validate if the query is weather-related about a city
                is_valid, error_message = is_weather_query(user_input)
                if not is_valid:
                    print(f"\nAgent: {error_message}\n")
                    continue
                
                # Invoke the agent
                response = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
                
                # Extract the response
                if "messages" in response:
                    last_message = response["messages"][-1]
                    if hasattr(last_message, 'content'):
                        print(f"\nAgent: {last_message.content}\n")
                    else:
                        print(f"\nAgent: {str(last_message)}\n")
                else:
                    print(f"\nAgent: {str(response)}\n")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"\nError: {str(e)}\n")
                
    except ValueError as e:
        print(f"Configuration Error: {str(e)}")
        print("Please ensure OPENAI_API_KEY is set in your .env file")
        sys.exit(1)


if __name__ == "__main__":
    main()
