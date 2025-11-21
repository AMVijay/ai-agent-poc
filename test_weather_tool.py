"""Test script for the weather agent."""

from weather_tool import get_weather


def test_weather_tool():
    """Test the weather tool independently."""
    print("Testing Weather Tool")
    print("=" * 50)
    
    cities = ["London", "Tokyo", "New York", "Paris", "Sydney"]
    
    for city in cities:
        print(f"\nFetching weather for {city}...")
        result = get_weather(city)
        print(result)
        print("-" * 50)


if __name__ == "__main__":
    test_weather_tool()
