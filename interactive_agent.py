"""Interactive weather agent using LangGraph."""

import os
import sys
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
        raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in .env file.")
    
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
