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
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your-api-key-here":
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    
    # Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        api_key=api_key
    )
    
    # Define the weather tool using decorator
    @tool
    def weather_tool(city: str) -> str:
        """Get current weather information for a US city only. Input should be a US city name."""
        return get_weather(city)
    
    # Create tool list
    tools = [weather_tool]
    
    # Create the agent using LangGraph
    agent = create_react_agent(
        llm,
        tools,
        state_modifier="You are a helpful weather assistant for US cities only. You can check weather information for cities in the United States using the available tools. If a user asks about weather in non-US cities, politely inform them that you only provide weather information for US cities. Provide clear and concise weather information."
    )
    
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
