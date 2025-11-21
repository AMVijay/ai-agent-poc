# 🚀 How to Run the Weather Agent

## Quick Start (3 Steps)

### Step 1: Set Up Your OpenAI API Key
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# nano .env
# (or use your favorite editor)
```

**In `.env` file:**
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Agent

Choose one of the three options below:

---

## Option A: Run Unit Tests (No API Key Needed!) ✅

Perfect for testing the US-only restriction without needing OpenAI API key.

```bash
# Run unit tests
python -m unittest test_us_restriction_unit.py -v

# Output:
# test_city_not_found .......................... ok
# test_non_us_city_rejected ................... ok
# test_paris_rejected ......................... ok
# test_tokyo_rejected ......................... ok
# test_us_city_success ........................ ok
# Ran 5 tests in 0.005s - OK
```

---

## Option B: Run Comprehensive Tests (No API Key Needed!) ✅

Tests weather tool with both US and non-US cities.

```bash
# Run comprehensive tests
python test_weather_comprehensive.py

# Output:
# TESTING US CITIES (Should show weather)
# 🇺🇸 Testing: New York
# Weather Information for New York, New York, United States:
# - Temperature: 15.5°C
# - Condition: Partly cloudy
# - Humidity: 70%
# - Wind Speed: 8.5 km/h
#
# TESTING NON-US CITIES (Should be REJECTED)
# ❌ Testing: London
# Sorry, 'London' is not a US city...
# ✅ CORRECTLY REJECTED (Non-US city)
```

---

## Option C: Run Demo Agent (Requires OpenAI API Key) 🔑

Runs pre-set example queries with the LangChain agent.

```bash
# Make sure .env file has your OpenAI API key
python weather_agent.py

# Output:
# 🌤️  Weather Agent initialized!
# ==================================================
# User: What's the weather like in New York?
# --------------------------------------------------
# Agent: [Uses tool-calling to get weather and respond]
# --------------------------------------------------
```

**Example Queries Tested:**
- "What's the weather like in New York?"
- "Tell me about the weather in Los Angeles"
- "How's the weather in Chicago today?"

---

## Option D: Interactive Agent (Requires OpenAI API Key) 🔑

Chat with the agent in real-time! Type any question about US weather.

```bash
# Make sure .env file has your OpenAI API key
python interactive_agent.py

# Output:
# 🌤️  Welcome to Weather Agent!
# ============================================================
# Ask me about the weather in any city.
# Type 'quit' or 'exit' to leave.
#
# You: What's the weather in Seattle?
# Agent: [Fetches and returns weather for Seattle]
#
# You: How's the weather in London?
# Agent: Sorry, 'London' is not a US city. This weather agent 
#        only provides weather information for US cities...
#
# You: quit
# Goodbye! 👋
```

---

## Which Option Should I Use?

| Option | Use Case | API Key? | Time |
|--------|----------|----------|------|
| **A: Unit Tests** | Test restriction logic | ❌ No | 5 sec |
| **B: Comprehensive Tests** | Test all scenarios | ❌ No | 1 sec |
| **C: Demo Agent** | See agent in action | ✅ Yes | 10 sec |
| **D: Interactive** | Play with agent live | ✅ Yes | ∞ |

---

## Step-by-Step Example: Getting Started

### 1. Clone/Setup
```bash
cd /workspaces/ai-agent-poc
```

### 2. Install packages
```bash
pip install -r requirements.txt
```

### 3. Quick test (no API key needed)
```bash
python test_weather_comprehensive.py
```

Expected output:
```
TESTING US CITIES (Should show weather)
===================================================================

🇺🇸 Testing: New York
Weather Information for New York, New York, United States:
- Temperature: 15.5°C
- Condition: Partly cloudy

✅ CORRECTLY REJECTED (Non-US city)
```

### 4. Get OpenAI API key (for interactive use)
- Go to https://platform.openai.com/api/keys
- Create a new API key
- Copy it

### 5. Add API key to .env
```bash
cp .env.example .env
# Edit .env and paste your API key
```

### 6. Run interactive agent
```bash
python interactive_agent.py
```

### 7. Ask questions!
```
You: What's the weather in Miami?
You: How's the weather in Boston?
You: Tell me about New York weather
You: quit
```

---

## Troubleshooting

### "OPENAI_API_KEY not found"
**Solution:** Make sure you have a `.env` file with your API key:
```bash
cp .env.example .env
# Then edit .env and add your actual API key
```

### "HTTPSConnectionPool timeout"
**Solution:** The Open-Meteo API might be slow. Try again - it usually works.

### "No module named langchain"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### "Connection refused"
**Solution:** Check your internet connection and OpenAI API key validity.

---

## Project Structure

```
ai-agent-poc/
├── weather_tool.py           # Core weather tool (US-only)
├── weather_agent.py          # Main demo agent
├── interactive_agent.py      # Interactive CLI
│
├── test_*.py                 # All test files
│   ├── test_us_restriction_unit.py      # Unit tests ✅
│   ├── test_weather_comprehensive.py    # Integration tests ✅
│   └── test_weather_tool.py             # Tool tests
│
├── requirements.txt          # Python dependencies
├── .env.example             # API key template
└── README.md                # Full documentation
```

---

## Features Summary

✅ LangChain agent with GPT-3.5-turbo  
✅ Tool-calling architecture  
✅ US-only city restriction  
✅ Real weather data (Open-Meteo API)  
✅ Natural language understanding  
✅ Error handling & retries  
✅ Multiple interaction modes  
✅ Comprehensive tests included  

---

## Commands Quick Reference

```bash
# Test without API key
python -m unittest test_us_restriction_unit.py -v
python test_weather_comprehensive.py

# Test with API key
python test_weather_tool.py

# Run agent with API key
python weather_agent.py          # Demo mode
python interactive_agent.py      # Interactive mode
```

---

## Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Run tests: `python test_weather_comprehensive.py`
3. ✅ Get API key: https://platform.openai.com/api/keys
4. ✅ Setup .env: `cp .env.example .env` (then add API key)
5. ✅ Run interactive: `python interactive_agent.py`

**Enjoy! 🌤️**
