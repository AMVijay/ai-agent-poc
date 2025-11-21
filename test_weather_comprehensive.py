"""Direct test of weather tool with mocked API responses."""

from unittest.mock import patch, MagicMock
from weather_tool import get_weather


def test_us_cities():
    """Test with real-like mock responses for US cities."""
    print("=" * 70)
    print("TESTING US CITIES (Should show weather)")
    print("=" * 70)
    
    us_cities = [
        ("New York", {"country": "United States", "country_code": "US", "admin1": "New York"}),
        ("Los Angeles", {"country": "United States", "country_code": "US", "admin1": "California"}),
        ("Chicago", {"country": "United States", "country_code": "US", "admin1": "Illinois"}),
    ]
    
    for city, geo_data in us_cities:
        print(f"\n🇺🇸 Testing: {city}")
        print("-" * 70)
        
        with patch('weather_tool.requests.get') as mock_get:
            # Mock geocoding response
            geo_response = MagicMock()
            geo_response.json.return_value = {
                'results': [
                    {
                        'name': city,
                        'latitude': 40.0,
                        'longitude': -74.0,
                        **geo_data
                    }
                ]
            }
            geo_response.raise_for_status.return_value = None
            
            # Mock weather response
            weather_response = MagicMock()
            weather_response.json.return_value = {
                'current': {
                    'temperature_2m': 15.5,
                    'relative_humidity_2m': 70,
                    'weather_code': 2,
                    'wind_speed_10m': 8.5
                }
            }
            weather_response.raise_for_status.return_value = None
            
            mock_get.side_effect = [geo_response, weather_response]
            
            result = get_weather(city)
            print(result)


def test_non_us_cities():
    """Test with mock responses for non-US cities."""
    print("\n\n" + "=" * 70)
    print("TESTING NON-US CITIES (Should be REJECTED)")
    print("=" * 70)
    
    non_us_cities = [
        ("London", {"country": "United Kingdom", "country_code": "GB"}),
        ("Tokyo", {"country": "Japan", "country_code": "JP"}),
        ("Paris", {"country": "France", "country_code": "FR"}),
        ("Sydney", {"country": "Australia", "country_code": "AU"}),
    ]
    
    for city, geo_data in non_us_cities:
        print(f"\n❌ Testing: {city}")
        print("-" * 70)
        
        with patch('weather_tool.requests.get') as mock_get:
            geo_response = MagicMock()
            geo_response.json.return_value = {
                'results': [
                    {
                        'name': city,
                        'latitude': 40.0,
                        'longitude': 74.0,
                        **geo_data
                    }
                ]
            }
            geo_response.raise_for_status.return_value = None
            mock_get.return_value = geo_response
            
            result = get_weather(city)
            print(result)
            
            # Verify rejection
            if "not a US city" in result:
                print("✅ CORRECTLY REJECTED (Non-US city)")
            else:
                print("❌ ERROR: Should have been rejected!")


def test_invalid_cities():
    """Test with non-existent cities."""
    print("\n\n" + "=" * 70)
    print("TESTING INVALID CITIES (Should show 'not found')")
    print("=" * 70)
    
    invalid_cities = ["XyzCity123", "FakeTown999", "NoSuchPlace"]
    
    for city in invalid_cities:
        print(f"\n🔍 Testing: {city}")
        print("-" * 70)
        
        with patch('weather_tool.requests.get') as mock_get:
            geo_response = MagicMock()
            geo_response.json.return_value = {'results': []}
            geo_response.raise_for_status.return_value = None
            mock_get.return_value = geo_response
            
            result = get_weather(city)
            print(result)


if __name__ == "__main__":
    test_us_cities()
    test_non_us_cities()
    test_invalid_cities()
    
    print("\n\n" + "=" * 70)
    print("✅ TESTING COMPLETE")
    print("=" * 70)
