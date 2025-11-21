"""Unit tests for the US-only weather restriction."""

import unittest
from unittest.mock import patch, MagicMock
from weather_tool import get_weather


class TestUSWeatherRestriction(unittest.TestCase):
    """Test cases for US-only weather restriction."""
    
    @patch('weather_tool.requests.get')
    def test_us_city_success(self, mock_get):
        """Test that US cities return weather successfully."""
        # Mock response for New York (US city)
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'results': [
                {
                    'name': 'New York',
                    'latitude': 40.7128,
                    'longitude': -74.0060,
                    'country': 'United States',
                    'country_code': 'US',
                    'admin1': 'New York'
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_weather("New York")
        self.assertIn("New York", result)
        self.assertIn("Temperature", result)
    
    @patch('weather_tool.requests.get')
    def test_non_us_city_rejected(self, mock_get):
        """Test that non-US cities are rejected."""
        # Mock response for London (non-US city)
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'results': [
                {
                    'name': 'London',
                    'latitude': 51.5074,
                    'longitude': -0.1278,
                    'country': 'United Kingdom',
                    'country_code': 'GB',
                    'admin1': 'England'
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_weather("London")
        self.assertIn("not a US city", result)
        self.assertIn("US cities", result)
    
    @patch('weather_tool.requests.get')
    def test_city_not_found(self, mock_get):
        """Test handling of non-existent cities."""
        # Mock empty response
        mock_response = MagicMock()
        mock_response.json.return_value = {'results': []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_weather("InvalidCity123")
        self.assertIn("not found", result)
    
    @patch('weather_tool.requests.get')
    def test_tokyo_rejected(self, mock_get):
        """Test that Tokyo (Japan) is rejected."""
        # Mock response for Tokyo (non-US city)
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'results': [
                {
                    'name': 'Tokyo',
                    'latitude': 35.6762,
                    'longitude': 139.6503,
                    'country': 'Japan',
                    'country_code': 'JP',
                    'admin1': 'Tokyo'
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_weather("Tokyo")
        self.assertIn("not a US city", result)
        self.assertNotIn("Temperature", result)
    
    @patch('weather_tool.requests.get')
    def test_paris_rejected(self, mock_get):
        """Test that Paris (France) is rejected."""
        # Mock response for Paris (non-US city)
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'results': [
                {
                    'name': 'Paris',
                    'latitude': 48.8566,
                    'longitude': 2.3522,
                    'country': 'France',
                    'country_code': 'FR',
                    'admin1': 'Île-de-France'
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_weather("Paris")
        self.assertIn("not a US city", result)
        self.assertIn("US cities", result)


if __name__ == '__main__':
    unittest.main()
