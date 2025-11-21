# 🔑 Setup Instructions for Interactive Agent

## Step 1: Get Your OpenAI API Key

1. Go to: https://platform.openai.com/api/keys
2. Sign in to your OpenAI account (create one if needed)
3. Click **"Create new secret key"**
4. Copy the key (starts with `sk-`)

## Step 2: Add API Key to .env

```bash
# Edit the .env file
nano .env
```

The file should look like:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

Save and exit (Ctrl+X, then Y, then Enter for nano)

## Step 3: Run Interactive Agent

```bash
python interactive_agent.py
```

You'll see:
```
🌤️  Welcome to Weather Agent!
============================================================
Ask me about the weather in any US city.
Type 'quit' or 'exit' to leave.

You: 
```

## Step 4: Chat with the Agent!

Try these questions:

**US Cities (Will Work):**
```
You: What's the weather in New York?
You: How's the weather in Los Angeles?
You: Tell me about Chicago weather
You: Weather in Seattle?
You: How's Miami today?
```

**Non-US Cities (Will Be Rejected):**
```
You: What's the weather in London?
Agent: Sorry, 'London' is not a US city...

You: How's Tokyo?
Agent: Sorry, 'Tokyo' is not a US city...
```

**Exit:**
```
You: quit
Goodbye! 👋
```

---

## Current Status

✅ Interactive agent code is ready  
✅ Weather tool is working  
✅ US-only restriction is implemented  

**What you need:**
❌ OpenAI API Key (get from https://platform.openai.com/api/keys)

Once you add the API key to .env and run `python interactive_agent.py`, you're all set!

---

## Don't Have an OpenAI Account?

1. Go to https://openai.com/
2. Click **"Sign up"**
3. Create account with email
4. Go to https://platform.openai.com/api/keys
5. Create a new secret key
6. You get free credits to start!

---

## Troubleshooting

**"OPENAI_API_KEY not found"**
- Make sure .env file has your actual API key, not `your-api-key-here`

**"Connection refused"**
- Check your internet connection
- Check your API key is correct

**Agent not responding**
- First check it's a valid OpenAI API key
- Make sure you have free credits on OpenAI account

---

## Can I Test Without API Key?

Yes! Run the tests (no API key needed):

```bash
# Quick comprehensive test
python test_weather_comprehensive.py

# Unit tests
python -m unittest test_us_restriction_unit.py -v
```

These will show you how the agent works without needing OpenAI API!
