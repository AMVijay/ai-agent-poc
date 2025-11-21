# Weather Agent with LangChain

A LangChain-based agent that can check weather information for US cities using natural language queries.

## Features

- 🌍 Check weather for any US city
- 🇺🇸 **US-only restriction** - Only provides weather for United States cities
- 🤖 Natural language interface powered by LangChain
- 🛠️ Custom weather tool using Open-Meteo API (free, no API key required)
- 📊 Current temperature, humidity, wind speed, and weather conditions
- ⚡ Fast and efficient agent execution

## Project Structure

```
├── weather_tool.py      # Weather fetching tool using Open-Meteo API
├── weather_agent.py     # LangChain agent implementation
├── test_weather_tool.py # Test script for the weather tool
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Installation

1. **Clone the repository and navigate to the project directory:**
   ```bash
   cd /workspaces/ai-agent-poc
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

## Usage

### Option 1: Test the Weather Tool Directly

```bash
python test_weather_tool.py
```

This will fetch weather information for multiple cities using the weather tool directly.

### Option 2: Run the LangChain Agent

```bash
python weather_agent.py
```

This will run the agent with example queries. The agent uses natural language to understand your request and fetch weather information.

### Option 3: Use the Agent in Your Code

```python
from weather_agent import create_weather_agent

# Create the agent
agent = create_weather_agent()

# Ask a question
response = agent.invoke({"input": "What's the weather in Paris?"})
print(response['output'])
```

## Components

### Weather Tool (`weather_tool.py`)

- Uses the **Open-Meteo API** (free, no authentication required)
- Gets geolocation from city name using geocoding API
- Fetches current weather data (temperature, humidity, wind speed, conditions)
- Maps weather codes to human-readable descriptions

### LangChain Agent (`weather_agent.py`)

- **LLM**: GPT-3.5-turbo from OpenAI
- **Tool**: Custom weather tool wrapped as a LangChain Tool
- **Agent Type**: Tool-calling agent with error handling
- **Prompt**: System prompt instructing the agent to be a helpful weather assistant

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

## Dependencies

- **langchain**: LLM framework
- **langchain-community**: Community tools and integrations
- **langchain-openai**: OpenAI integration
- **openai**: OpenAI API client
- **python-dotenv**: Environment variable management
- **requests**: HTTP requests library

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

## Future Enhancements

- Add forecast data (5-day, 7-day, 14-day)
- Add severe weather alerts
- Add air quality information
- Support for multiple cities in a single query
- Add weather comparison between cities
- Implement response caching to reduce API calls
