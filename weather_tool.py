"""Weather tool for checking weather information based on US city only."""

import requests
from typing import Optional


def get_weather(city: str) -> str:
    """
    Get weather information for a given US city only.
    
    Args:
        city: US city name to check weather for
        
    Returns:
        Weather information as a string or error message if city is not in US
    """
    try:
        # Using Open-Meteo API (free, no API key required)
        # First, get coordinates for the city with admin level 2 to get more accurate results
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=en&format=json&admin_divisions=true"
        
        geo_response = requests.get(geocoding_url, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            return f"City '{city}' not found. Please check the spelling and try again."
        
        # Find the first US location - check both country and admin1 codes
        location = None
        for result in geo_data.get("results", []):
            country_code = result.get("country_code", "").upper()
            country = result.get("country", "").upper()
            admin1_name = result.get("admin1", "")
            
            # Check if it's a US city by country code or name
            is_us = country_code == "US" or "UNITED STATES" in country or "USA" in country
            
            if is_us:
                location = result
                break
        
        if not location:
            return f"Sorry, '{city}' is not a US city. This weather agent only provides weather information for US cities. Please enter a US city name."
        
        latitude = location["latitude"]
        longitude = location["longitude"]
        country = location.get("country", "")
        state = location.get("admin1", "")
        
        # Get weather data
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&temperature_unit=celsius"
        
        weather_response = requests.get(weather_url, timeout=5)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        current = weather_data.get("current", {})
        
        # Map weather codes to descriptions
        weather_descriptions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail",
        }
        
        weather_code = current.get("weather_code", 0)
        weather_description = weather_descriptions.get(weather_code, "Unknown")
        
        temperature = current.get("temperature_2m", "N/A")
        humidity = current.get("relative_humidity_2m", "N/A")
        wind_speed = current.get("wind_speed_10m", "N/A")
        
        result = f"""
Weather Information for {city}, {state}, {country}:
- Temperature: {temperature}°C
- Condition: {weather_description}
- Humidity: {humidity}%
- Wind Speed: {wind_speed} km/h
        """
        return result.strip()
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"
    except Exception as e:
        return f"Error processing weather data: {str(e)}"


if __name__ == "__main__":
    # Test the weather tool
    print(get_weather("New York"))
    print()
    print(get_weather("Los Angeles"))
    print()
    print(get_weather("Chicago"))
