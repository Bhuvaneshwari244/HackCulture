"""
Real-time Weather Service Integration
Supports OpenWeatherMap and WeatherAPI.com
"""

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class WeatherService:
    def __init__(self):
        """Initialize weather service with API keys"""
        self.openweather_key = os.getenv('OPENWEATHER_API_KEY', '')
        self.weatherapi_key = os.getenv('WEATHERAPI_KEY', '')
        
        # API endpoints
        self.openweather_url = "https://api.openweathermap.org/data/2.5"
        self.weatherapi_url = "https://api.weatherapi.com/v1"
        
    def get_weather_forecast(self, location):
        """
        Get weather forecast for location
        
        Parameters:
        - location: dict with latitude, longitude, or city name
        
        Returns weather forecast data
        """
        # Try OpenWeatherMap first (you have a valid key for this)
        if self.openweather_key and self.openweather_key != 'demo_key_get_yours_at_openweathermap_org':
            try:
                return self._get_openweather_forecast(location)
            except Exception as e:
                print(f"OpenWeatherMap failed: {e}, trying WeatherAPI...")
        
        # Try WeatherAPI as fallback
        if self.weatherapi_key and self.weatherapi_key != 'demo_key_get_yours_at_weatherapi_com':
            try:
                return self._get_weatherapi_forecast(location)
            except Exception as e:
                print(f"WeatherAPI failed: {e}, using mock data...")
        
        # Return mock data if APIs not configured
        return self._get_mock_forecast(location)
    
    def _get_weatherapi_forecast(self, location):
        """Get forecast from WeatherAPI.com (FREE: 1M calls/month)"""
        # Determine query parameter
        if 'latitude' in location and 'longitude' in location:
            query = f"{location['latitude']},{location['longitude']}"
        elif 'city' in location:
            query = location['city']
        elif 'district' in location and 'state' in location:
            query = f"{location['district']},{location['state']},India"
        else:
            raise ValueError("Invalid location format")
        
        # Call API
        url = f"{self.weatherapi_url}/forecast.json"
        params = {
            'key': self.weatherapi_key,
            'q': query,
            'days': 7,
            'aqi': 'no',
            'alerts': 'yes'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Parse response
        current = data['current']
        forecast = data['forecast']['forecastday']
        alerts = data.get('alerts', {}).get('alert', [])
        
        # Calculate rainfall probability
        rainfall_prob = sum([day['day']['daily_chance_of_rain'] for day in forecast]) / len(forecast)
        
        # Check for extreme weather
        extreme_weather = len(alerts) > 0 or any(
            day['day']['maxwind_kph'] > 40 or 
            day['day']['daily_chance_of_rain'] > 80 
            for day in forecast
        )
        
        return {
            'source': 'WeatherAPI.com',
            'next_7_days': {
                'rainfall_probability': int(rainfall_prob),
                'avg_temperature': current['temp_c'],
                'humidity': current['humidity'],
                'extreme_weather_alert': extreme_weather
            },
            'season_outlook': {
                'rainfall': 'Heavy' if rainfall_prob > 70 else 'Normal' if rainfall_prob > 40 else 'Low',
                'temperature': 'Above Normal' if current['temp_c'] > 30 else 'Normal',
                'overall': 'Favorable' if not extreme_weather else 'Caution Advised'
            },
            'alerts': [
                {
                    'type': alert.get('event', 'weather'),
                    'severity': alert.get('severity', 'moderate'),
                    'message': alert.get('headline', 'Weather alert in your area')
                }
                for alert in alerts
            ] if alerts else [],
            'detailed_forecast': [
                {
                    'date': day['date'],
                    'max_temp': day['day']['maxtemp_c'],
                    'min_temp': day['day']['mintemp_c'],
                    'rain_chance': day['day']['daily_chance_of_rain'],
                    'condition': day['day']['condition']['text']
                }
                for day in forecast
            ]
        }
    
    def _get_openweather_forecast(self, location):
        """Get forecast from OpenWeatherMap (FREE: 60 calls/min)"""
        lat = location.get('latitude', 28.7041)
        lon = location.get('longitude', 77.1025)
        
        # Call current weather API
        url = f"{self.openweather_url}/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.openweather_key,
            'units': 'metric'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        current_data = response.json()
        
        # Extract location name from response
        location_name = current_data.get('name', 'Unknown')
        if not location_name or location_name == 'Unknown':
            # Try to get from sys info
            location_name = location.get('district', 'Your Location')
        
        # Call forecast API (5 day / 3 hour)
        forecast_url = f"{self.openweather_url}/forecast"
        forecast_response = requests.get(forecast_url, params=params, timeout=10)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        
        # Calculate rainfall probability from forecast
        rain_forecasts = [
            item.get('pop', 0) * 100 
            for item in forecast_data['list'][:24]  # Next 3 days
        ]
        rainfall_prob = sum(rain_forecasts) / len(rain_forecasts) if rain_forecasts else 0
        
        # Check for extreme weather
        extreme_weather = (
            current_data['wind']['speed'] > 15 or  # High wind
            rainfall_prob > 80 or  # Heavy rain expected
            current_data['main']['temp'] > 40  # Extreme heat
        )
        
        return {
            'source': 'OpenWeatherMap',
            'location_name': location_name,
            'next_7_days': {
                'rainfall_probability': int(rainfall_prob),
                'avg_temperature': current_data['main']['temp'],
                'humidity': current_data['main']['humidity'],
                'extreme_weather_alert': extreme_weather
            },
            'season_outlook': {
                'rainfall': 'Heavy' if rainfall_prob > 70 else 'Normal' if rainfall_prob > 40 else 'Low',
                'temperature': 'Above Normal' if current_data['main']['temp'] > 30 else 'Normal',
                'overall': 'Favorable' if not extreme_weather else 'Caution Advised'
            },
            'alerts': [
                {
                    'type': 'extreme_weather',
                    'severity': 'high',
                    'message': 'Extreme weather conditions detected'
                }
            ] if extreme_weather else [],
            'current_conditions': {
                'temperature': current_data['main']['temp'],
                'feels_like': current_data['main']['feels_like'],
                'humidity': current_data['main']['humidity'],
                'pressure': current_data['main']['pressure'],
                'wind_speed': current_data['wind']['speed'],
                'description': current_data['weather'][0]['description']
            }
        }
    
    def _get_mock_forecast(self, location):
        """Return mock forecast data when APIs not available"""
        return {
            'source': 'Mock Data (Configure API keys for real data)',
            'next_7_days': {
                'rainfall_probability': 60,
                'avg_temperature': 28,
                'humidity': 65,
                'extreme_weather_alert': False
            },
            'season_outlook': {
                'rainfall': 'Normal',
                'temperature': 'Normal',
                'overall': 'Favorable'
            },
            'alerts': [],
            'note': 'Using simulated data. Add API keys in .env file for real weather updates.'
        }


# Example usage and testing
if __name__ == '__main__':
    weather_service = WeatherService()
    
    print("=" * 70)
    print("Weather Service Test")
    print("=" * 70)
    
    # Test location
    test_location = {
        'latitude': 28.7041,
        'longitude': 77.1025,
        'district': 'Delhi',
        'state': 'Delhi'
    }
    
    print(f"\nTesting weather for: Delhi")
    print("-" * 70)
    
    forecast = weather_service.get_weather_forecast(test_location)
    
    print(f"\nData Source: {forecast['source']}")
    print(f"\n7-Day Outlook:")
    print(f"  Rainfall Probability: {forecast['next_7_days']['rainfall_probability']}%")
    print(f"  Avg Temperature: {forecast['next_7_days']['avg_temperature']}°C")
    print(f"  Humidity: {forecast['next_7_days']['humidity']}%")
    print(f"  Extreme Weather: {'Yes' if forecast['next_7_days']['extreme_weather_alert'] else 'No'}")
    
    print(f"\nSeason Outlook:")
    print(f"  Rainfall: {forecast['season_outlook']['rainfall']}")
    print(f"  Temperature: {forecast['season_outlook']['temperature']}")
    print(f"  Overall: {forecast['season_outlook']['overall']}")
    
    if forecast['alerts']:
        print(f"\n⚠️  Alerts:")
        for alert in forecast['alerts']:
            print(f"  - {alert['message']}")
    
    if 'note' in forecast:
        print(f"\n📝 Note: {forecast['note']}")
    
    print("\n" + "=" * 70)
    print("To get real weather data:")
    print("1. Sign up at https://www.weatherapi.com/signup.aspx (FREE)")
    print("2. Copy your API key")
    print("3. Add to backend/.env: WEATHERAPI_KEY=your_key_here")
    print("4. Restart the backend server")
    print("=" * 70)
