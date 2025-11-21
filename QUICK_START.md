# 📖 Quick Start Guide - 5 Minutes to Running the Weather Agent

## 🎯 Goal
Get the weather agent running and understand how it works.

---

## ⚡ 5-Minute Quick Start

### Step 1: Navigate to project (30 seconds)
```bash
cd /workspaces/ai-agent-poc
```

### Step 2: Install dependencies (2 minutes)
```bash
pip install -r requirements.txt
```

### Step 3: Run tests (30 seconds)
```bash
# Test without needing API key
python test_weather_comprehensive.py
```

**What you'll see:**
```
✅ New York weather: Temperature 15.5°C, Partly cloudy
✅ Los Angeles weather: Temperature 15.5°C, Partly cloudy
✅ Chicago weather: Temperature 15.5°C, Partly cloudy

❌ London REJECTED: "Sorry, 'London' is not a US city..."
❌ Tokyo REJECTED: "Sorry, 'Tokyo' is not a US city..."
❌ Paris REJECTED: "Sorry, 'Paris' is not a US city..."

✅ Invalid cities show: "City 'XyzCity' not found"
```

**Done! You've successfully tested the agent.** ✅

---

## 🔑 Want to Use the Live Agent? (Optional - 2 more minutes)

### Step 4: Get OpenAI API Key
1. Go to https://platform.openai.com/api/keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)

### Step 5: Set up .env file
```bash
cp .env.example .env
# Now edit .env and paste your API key
nano .env
# (or use your favorite editor)
```

**Edit `.env` to look like:**
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### Step 6: Run interactive agent
```bash
python interactive_agent.py
```

**You'll see:**
```
🌤️  Welcome to Weather Agent!
============================================================
Ask me about the weather in any city.
Type 'quit' or 'exit' to leave.

You: What's the weather in Miami?
Agent: [Gets weather for Miami from the tool]

You: How's London?
Agent: Sorry, 'London' is not a US city...

You: quit
Goodbye! 👋
```

---

## 📊 What Just Happened?

Your weather agent:

1. **Accepts US cities** → Returns real weather data
2. **Rejects non-US cities** → Explains it's US-only
3. **Handles invalid cities** → Shows "not found" message
4. **Uses LangChain** → Natural language understanding
5. **Uses GPT-3.5-turbo** → Smart responses
6. **Calls weather tool** → Gets real API data

---

## 🎮 Try These Commands

### No API Key Needed:
```bash
# Run unit tests (5 tests)
python -m unittest test_us_restriction_unit.py -v

# Run comprehensive demo (11 scenarios)
python test_weather_comprehensive.py

# See all test reports
cat TEST_REPORT.md
cat TESTING_SUMMARY.md
```

### With API Key:
```bash
# Run agent demo with example queries
python weather_agent.py

# Interactive chat mode
python interactive_agent.py

# Direct tool test
python test_weather_tool.py
```

---

## 📁 File Guide

| File | Purpose | Run Command |
|------|---------|------------|
| `weather_tool.py` | Core tool (fetches weather) | Used by agent |
| `weather_agent.py` | Demo agent | `python weather_agent.py` |
| `interactive_agent.py` | Chat mode | `python interactive_agent.py` |
| `test_us_restriction_unit.py` | Unit tests | `python -m unittest test_us_restriction_unit.py -v` |
| `test_weather_comprehensive.py` | Integration tests | `python test_weather_comprehensive.py` |
| `requirements.txt` | Dependencies | `pip install -r requirements.txt` |
| `.env.example` | Config template | Copy to `.env` |
| `README.md` | Full docs | Read in VS Code |

---

## ✅ Verification Checklist

After running tests, you should see:

- [x] US cities return weather (New York, Los Angeles, Chicago)
- [x] Non-US cities are rejected (London, Tokyo, Paris, Sydney)
- [x] Invalid cities show "not found" message
- [x] All 5 unit tests pass
- [x] All 11 comprehensive scenarios pass
- [x] Clear, helpful error messages

If you see all these ✅, the agent is working perfectly!

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | Run `pip install -r requirements.txt` |
| OPENAI_API_KEY not found | Create `.env` file with your API key |
| Connection timeout | Try again (external API may be slow) |
| Permission denied | Use `python` instead of `python3` |

---

## 🚀 What's Next?

### Explore the Code:
```bash
cat weather_tool.py        # See how weather is fetched
cat weather_agent.py       # See LangChain agent setup
cat interactive_agent.py   # See interactive mode
```

### Read Full Documentation:
- `README.md` - Full project overview
- `HOW_TO_RUN.md` - Detailed running instructions
- `TEST_REPORT.md` - Test results
- `US_RESTRICTION_IMPLEMENTATION.md` - Technical details

### Customize:
- Edit city list in `weather_agent.py`
- Change system prompt in agents
- Add more weather data fields
- Integrate with other tools

---

## 📞 Quick Reference

```bash
# Install
pip install -r requirements.txt

# Test (no API key needed)
python test_weather_comprehensive.py

# Setup API key
cp .env.example .env
nano .env  # edit and paste your key

# Run interactive
python interactive_agent.py

# View docs
cat HOW_TO_RUN.md
cat README.md
```

---

**Ready to get started? Run this now:**

```bash
cd /workspaces/ai-agent-poc && python test_weather_comprehensive.py
```

You'll see the agent in action in 30 seconds! ⚡
