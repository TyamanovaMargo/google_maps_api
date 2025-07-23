"""
Configuration file template for Google Maps Places API Search

INSTRUCTIONS:
1. Copy this file to config.py
2. Replace "YOUR_API_KEY_HERE" with your actual Google Maps API key
3. Customize default settings if needed

DO NOT commit config.py with real API keys to version control!
"""

# Google Maps API Configuration
GOOGLE_MAPS_API_KEY = "YOUR_API_KEY_HERE"

# Default search settings (optional - can be overridden by user input)
DEFAULT_SETTINGS = {
    "radius": "1000",  # Default search radius in meters
    "output_file": "places_results.json",  # Default output filename
}

# Example locations (for quick testing)
EXAMPLE_LOCATIONS = {
    "new_york": {
        "latitude": "40.7128",
        "longitude": "-74.0060",
        "description": "New York City, USA"
    },
    "london": {
        "latitude": "51.5074",
        "longitude": "-0.1278", 
        "description": "London, UK"
    },
    "tokyo": {
        "latitude": "35.6762",
        "longitude": "139.6503",
        "description": "Tokyo, Japan"
    },
    "paris": {
        "latitude": "48.8566",
        "longitude": "2.3522",
        "description": "Paris, France"
    },
    "moscow": {
        "latitude": "55.7558",
        "longitude": "37.6173",
        "description": "Moscow, Russia"
    },
    "sydney": {
        "latitude": "-33.8688",
        "longitude": "151.2093",
        "description": "Sydney, Australia"
    }
}