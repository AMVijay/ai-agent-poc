"""Test script to verify US-only weather restriction."""

from weather_tool import get_weather


def test_us_cities():
    """Test weather tool with US cities."""
    print("Testing US Cities (should work)")
    print("=" * 60)
    
    us_cities = ["New York", "Los Angeles", "Chicago", "Houston", "Miami"]
    
    for city in us_cities:
        print(f"\n📍 {city}:")
        result = get_weather(city)
        print(result)
        print("-" * 60)


def test_non_us_cities():
    """Test weather tool with non-US cities."""
    print("\n\nTesting Non-US Cities (should be rejected)")
    print("=" * 60)
    
    non_us_cities = ["London", "Tokyo", "Paris", "Sydney", "Toronto"]
    
    for city in non_us_cities:
        print(f"\n🌍 {city}:")
        result = get_weather(city)
        print(result)
        print("-" * 60)


if __name__ == "__main__":
    test_us_cities()
    test_non_us_cities()
