"""
Utility Functions for Google Maps Places API Search

This module contains utility functions for data validation,
file operations, and other helper functions.
"""

import json
import os
from typing import List, Dict
from datetime import datetime


def validate_user_input(user_input: Dict[str, str]) -> bool:
    """
    Validate user input parameters for API search.
    
    Args:
        user_input (dict): Dictionary containing user input parameters
    
    Returns:
        bool: True if all inputs are valid, False otherwise
    """
    # Check if all required fields are provided
    required_fields = ['api_key', 'latitude', 'longitude', 'keyword', 'radius']
    for field in required_fields:
        if not user_input.get(field) or not user_input[field].strip():
            print(f"❌ Error: {field} is required and cannot be empty")
            return False
    
    # Validate API key format (basic check)
    api_key = user_input['api_key'].strip()
    if len(api_key) < 20:  # Google API keys are typically much longer
        print("⚠️ Warning: API key seems too short. Please verify it's correct.")
    
    # Validate latitude
    try:
        latitude = float(user_input['latitude'])
        if not (-90 <= latitude <= 90):
            print("❌ Error: Latitude must be between -90 and 90 degrees")
            return False
    except ValueError:
        print("❌ Error: Latitude must be a valid number")
        return False
    
    # Validate longitude
    try:
        longitude = float(user_input['longitude'])
        if not (-180 <= longitude <= 180):
            print("❌ Error: Longitude must be between -180 and 180 degrees")
            return False
    except ValueError:
        print("❌ Error: Longitude must be a valid number")
        return False
    
    # Validate radius
    try:
        radius = int(user_input['radius'])
        if not (1 <= radius <= 50000):
            print("❌ Error: Radius must be between 1 and 50,000 meters")
            return False
    except ValueError:
        print("❌ Error: Radius must be a valid whole number")
        return False
    
    # Validate keyword (basic check)
    keyword = user_input['keyword'].strip()
    if len(keyword) < 2:
        print("❌ Error: Keyword must be at least 2 characters long")
        return False
    
    # Check output filename
    output_file = user_input.get('output_file', 'places_results.json')
    if not output_file.endswith('.json'):
        print("⚠️ Warning: Output filename should end with '.json'")
    
    return True


def save_results_to_json(places_data: List[Dict], filename: str = "places_results.json") -> bool:
    """
    Save places data to a JSON file with metadata.
    
    Args:
        places_data (list): List of place dictionaries to save
        filename (str): Output filename
    
    Returns:
        bool: True if save was successful, False otherwise
    """
    try:
        # Create output data structure with metadata
        output_data = {
            "metadata": {
                "search_timestamp": datetime.now().isoformat(),
                "total_places": len(places_data),
                "file_version": "1.0"
            },
            "places": places_data
        }
        
        # Ensure directory exists
        directory = os.path.dirname(filename) if os.path.dirname(filename) else '.'
        if directory != '.' and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Write JSON file with proper formatting
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(output_data, file, indent=2, ensure_ascii=False)
        
        # Verify file was written successfully
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            print(f"✅ Successfully saved {len(places_data)} places to {filename}")
            return True
        else:
            print(f"❌ Error: File {filename} was not created properly")
            return False
            
    except PermissionError:
        print(f"❌ Error: Permission denied writing to {filename}")
        return False
    except IOError as e:
        print(f"❌ Error saving to {filename}: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error saving file: {e}")
        return False


def load_results_from_json(filename: str) -> List[Dict]:
    """
    Load places data from a JSON file.
    
    Args:
        filename (str): Input filename
    
    Returns:
        list: List of place dictionaries, or empty list if load fails
    """
    try:
        if not os.path.exists(filename):
            print(f"❌ Error: File {filename} not found")
            return []
        
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Handle both old format (direct list) and new format (with metadata)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'places' in data:
            return data['places']
        else:
            print(f"❌ Error: Invalid file format in {filename}")
            return []
            
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {filename}: {e}")
        return []
    except Exception as e:
        print(f"❌ Error loading {filename}: {e}")
        return []


def format_distance(distance_meters: float) -> str:
    """
    Format distance in meters to human-readable format.
    
    Args:
        distance_meters (float): Distance in meters
    
    Returns:
        str: Formatted distance string
    """
    if distance_meters < 1000:
        return f"{distance_meters:.0f}m"
    else:
        return f"{distance_meters / 1000:.1f}km"


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the distance between two points using Haversine formula.
    
    Args:
        lat1, lon1: Latitude and longitude of first point
        lat2, lon2: Latitude and longitude of second point
    
    Returns:
        float: Distance in meters
    """
    import math
    
    # Convert latitude and longitude to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of Earth in meters
    earth_radius = 6371000
    
    return earth_radius * c


def validate_coordinates(latitude: str, longitude: str) -> tuple:
    """
    Validate and convert coordinate strings to float values.
    
    Args:
        latitude (str): Latitude as string
        longitude (str): Longitude as string
    
    Returns:
        tuple: (lat, lon) as floats, or (None, None) if invalid
    """
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return lat, lon
        else:
            return None, None
            
    except ValueError:
        return None, None


def create_sample_config() -> Dict:
    """
    Create a sample configuration dictionary for testing.
    
    Returns:
        dict: Sample configuration with example values
    """
    return {
        "api_key": "YOUR_GOOGLE_MAPS_API_KEY_HERE",
        "latitude": "40.7128",  # New York City
        "longitude": "-74.0060",
        "keyword": "restaurant",
        "radius": "1000",
        "output_file": "sample_results.json"
    }


def print_places_summary(places_data: List[Dict]) -> None:
    """
    Print a formatted summary of places data.
    
    Args:
        places_data (list): List of place dictionaries
    """
    if not places_data:
        print("No places to display.")
        return
    
    print(f"\n📋 PLACES SUMMARY ({len(places_data)} total)")
    print("=" * 60)
    
    for i, place in enumerate(places_data, 1):
        print(f"{i:2d}. {place['name']}")
        print(f"    📍 {place['address']}")
        print(f"    🌐 {place['latitude']}, {place['longitude']}")
        if i < len(places_data):
            print()
    
    print("=" * 60)