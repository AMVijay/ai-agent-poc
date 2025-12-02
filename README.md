# Weather Agent with LangChain

A LangChain-based agent that can check weather information for US cities using natural language queries. Works with GitHub Models API in Codespaces or OpenAI API.

## Features

- 🌍 Check weather for any US city
- 🇺🇸 **US-only restriction** - Only provides weather for United States cities
- 🤖 Natural language interface powered by LangChain
- 🛠️ Custom weather tool using Open-Meteo API (free, no API key required)
- 📊 Current temperature, humidity, wind speed, and weather conditions
- ⚡ Fast and efficient agent execution
- 🆓 **Free in Codespaces** - Uses GitHub Models API automatically
- 📱 Interactive command-line interface

## Project Structure

```
├── weather_tool.py      # Weather fetching tool using Open-Meteo API
├── weather_agent.py     # LangChain agent for standalone weather queries
├── interactive_agent.py # Interactive command-line weather agent
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment (optional for Codespaces):**
   ```bash
   cp .env.example .env
   ```
   
   - **In GitHub Codespaces**: No setup needed! Uses `GITHUB_TOKEN` automatically
   - **Locally**: Add your OpenAI API key to `.env`:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```

## Usage

### Option 1: Interactive Weather Agent

```bash
python interactive_agent.py
```

This starts an interactive command-line interface where you can ask weather questions. Type `quit` or `exit` to leave.

Example:
```
You: What's the weather in New York?
Agent: The weather in New York is currently...

You: Tell me about Chicago
Agent: Chicago is experiencing...

You: exit
Goodbye! 👋
```

### Option 2: Standalone Weather Agent

```bash
python weather_agent.py
```

This runs the agent with predefined example queries and displays weather information for multiple US cities.

### Option 3: Use the Agent in Your Code

```python
from interactive_agent import create_weather_agent

# Create the agent
agent = create_weather_agent()

# Ask a question
response = agent.invoke({"messages": [{"role": "user", "content": "What's the weather in New York?"}]})

# Extract response
last_message = response["messages"][-1]
print(last_message.content)
```

## Components

### Weather Tool (`weather_tool.py`)

- Uses the **Open-Meteo API** (free, no authentication required)
- Gets geolocation from city name using geocoding API
- Fetches current weather data (temperature, humidity, wind speed, conditions)
- Maps weather codes to human-readable descriptions

### Weather Agent (`weather_agent.py`)

- Standalone script for weather queries
- **LLM**: GitHub Models API (gpt-4o-mini) in Codespaces, or GPT-3.5-turbo from OpenAI
- **Tool**: Custom weather tool wrapped as a LangChain Tool
- **Agent Type**: Reactive agent with error handling
- Runs predefined example queries

### Interactive Agent (`interactive_agent.py`)

- Command-line interface for interactive weather queries
- **LLM**: GitHub Models API (gpt-4o-mini) in Codespaces, or GPT-3.5-turbo from OpenAI
- **Tool**: Custom weather tool wrapped as a LangChain Tool
- Accepts user input in a loop until user exits
- Shows which API is being used on startup

## Example Interactions

```
User: "What's the weather like in New York?"
Agent: The weather in New York, New York, United States is currently clear 
       with a temperature of 12°C, 65% humidity, and 8 km/h wind speed.

User: "How's the weather in Los Angeles?"
Agent: In Los Angeles, California, United States, it's partly cloudy with a 
       temperature of 18°C, 72% humidity, and 5 km/h wind speed.

User: "Tell me about weather in Chicago"
Agent: Chicago, Illinois, United States is experiencing overcast conditions 
       with a temperature of 8°C, 58% humidity, and 12 km/h wind speed.

User: "What about London?"
Agent: Sorry, 'London' is not a US city. This weather agent only provides 
       weather information for US cities. Please enter a US city name.
```

## API Support

### GitHub Models (Codespaces - Free)
- **Model**: gpt-4o-mini
- **Endpoint**: https://models.inference.ai.azure.com
- **Authentication**: Uses `GITHUB_TOKEN` (automatically available in Codespaces)
- **Cost**: Free

### OpenAI (Local Development)
- **Model**: gpt-3.5-turbo
- **Authentication**: Requires `OPENAI_API_KEY` in `.env`
- **Cost**: Paid

The agents automatically detect and use the appropriate API based on available credentials.

## Dependencies
## Notes

- The weather tool is **restricted to US cities only** - any attempt to get weather for non-US cities will be rejected
- The agent will automatically inform users about the US-only restriction
- The weather tool uses the free **Open-Meteo API**, which doesn't require authentication
- **In GitHub Codespaces**: Uses GitHub Models API automatically (no API key needed!)
- **Locally**: Requires an OpenAI API key for the GPT-3.5-turbo model
- Weather data is based on current conditions and is real-time
- LangGraph v1.0+ uses `create_react_agent` which may show deprecation warnings (code still works)
## API References

- **Open-Meteo Geocoding API**: https://open-meteo.com/en/docs/geocoding-api
- **Open-Meteo Weather API**: https://open-meteo.com/en/docs
- **LangChain Documentation**: https://python.langchain.com/
- **OpenAI API**: https://platform.openai.com/

## Notes

- The weather tool is **restricted to US cities only** - any attempt to get weather for non-US cities will be rejected
- The agent will automatically inform users about the US-only restriction
- The weather tool uses the free **Open-Meteo API**, which doesn't require authentication
- The LangChain agent requires an OpenAI API key for the GPT-3.5-turbo model
- Weather data is based on current conditions and is real-time
- The agent will retry up to 3 times if there are parsing errors
## Running in GitHub Codespaces

This project is optimized for GitHub Codespaces:

1. Open in Codespaces
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python interactive_agent.py`
4. That's it! Uses your GitHub token automatically - no API keys needed!

## Future Enhancements

- Add forecast data (5-day, 7-day, 14-day)
- Add severe weather alerts
- Add air quality information
- Support for multiple cities in a single query
- Add weather comparison between cities
- Implement response caching to reduce API calls
- Update to use latest LangChain agents module
- Implement response caching to reduce API calls
