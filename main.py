#!/usr/bin/env python3
"""
Google Maps Places API Search - Main CLI Script

This script provides a command-line interface for searching places using
the Google Maps Places API. It collects user input and orchestrates the
search process using functions from other modules.
"""

import sys
from places_api import PlacesAPIClient
from utils import save_results_to_json, validate_user_input
from config import GOOGLE_MAPS_API_KEY, DEFAULT_SETTINGS, EXAMPLE_LOCATIONS


def show_example_locations():
    """
    Display available example locations for quick testing.
    """
    print("\n📍 Example locations for quick testing:")
    print("-" * 40)
    for key, location in EXAMPLE_LOCATIONS.items():
        print(f"{key}: {location['description']} ({location['latitude']}, {location['longitude']})")
    print("-" * 40)


def get_user_input():
    """
    Collect user input for API parameters via command line interface.
    
    Returns:
        dict: Dictionary containing user input parameters
    """
    print("=" * 50)
    print("Google Maps Places API Search Tool")
    print("=" * 50)
    print()
    
    # Check if API key is configured
    if GOOGLE_MAPS_API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️  API key not configured!")
        print("Please edit config.py and add your Google Maps API key.")
        print()
        api_key = input("Or enter your API key now: ").strip()
    else:
        print("✅ Using API key from config.py")
        use_config_key = input("Use configured API key? (y/n, default: y): ").strip().lower()
        if use_config_key in ['', 'y', 'yes']:
            api_key = GOOGLE_MAPS_API_KEY
        else:
            api_key = input("Enter your Google Maps API Key: ").strip()
    
    # Show example locations
    show_locations = input("\nShow example locations? (y/n, default: n): ").strip().lower()
    if show_locations in ['y', 'yes']:
        show_example_locations()
        
        use_example = input("\nUse example location? Enter key (or 'n' for custom): ").strip().lower()
        if use_example in EXAMPLE_LOCATIONS:
            location = EXAMPLE_LOCATIONS[use_example]
            latitude = location['latitude']
            longitude = location['longitude']
            print(f"Using {location['description']}: {latitude}, {longitude}")
        else:
            print("Enter custom coordinates:")
            latitude = input("Latitude: ").strip()
            longitude = input("Longitude: ").strip()
    else:
        # Collect location coordinates
        print("\nEnter location coordinates:")
        latitude = input("Latitude: ").strip()
        longitude = input("Longitude: ").strip()
    
    # Collect search parameters
    keyword = input("\nEnter search keyword (e.g., 'restaurant', 'hospital', 'cafe'): ").strip()
    
    # Radius with default value
    default_radius = DEFAULT_SETTINGS.get('radius', '1000')
    radius = input(f"Enter search radius in meters (1-50000, default: {default_radius}): ").strip()
    if not radius:
        radius = default_radius
    
    # Optional: output filename with default
    default_filename = DEFAULT_SETTINGS.get('output_file', 'places_results.json')
    output_file = input(f"Enter output filename (default: {default_filename}): ").strip()
    if not output_file:
        output_file = default_filename
    
    return {
        'api_key': api_key,
        'latitude': latitude,
        'longitude': longitude,
        'keyword': keyword,
        'radius': radius,
        'output_file': output_file
    }


def display_search_summary(user_input):
    """
    Display a summary of the search parameters before starting.
    
    Args:
        user_input (dict): Dictionary containing user input parameters
    """
    print("\n" + "-" * 40)
    print("SEARCH SUMMARY")
    print("-" * 40)
    print(f"Location: {user_input['latitude']}, {user_input['longitude']}")
    print(f"Keyword: {user_input['keyword']}")
    print(f"Radius: {user_input['radius']} meters")
    print(f"Output file: {user_input['output_file']}")
    print("-" * 40)
    print()


def display_results_summary(places_data):
    """
    Display a summary of the search results.
    
    Args:
        places_data (list): List of place dictionaries
    """
    if not places_data:
        print("No places found matching your criteria.")
        return
    
    print(f"\n✅ Found {len(places_data)} places!")
    print("\nFirst 5 results:")
    print("-" * 40)
    
    # Display first 5 results as preview
    for i, place in enumerate(places_data[:5], 1):
        print(f"{i}. {place['name']}")
        print(f"   📍 {place['address']}")
        print(f"   🌐 {place['latitude']}, {place['longitude']}")
        print()
    
    if len(places_data) > 5:
        print(f"... and {len(places_data) - 5} more places")


def main():
    """
    Main function that orchestrates the entire search process.
    """
    try:
        # Step 1: Get user input
        user_input = get_user_input()
        
        # Step 2: Validate input
        if not validate_user_input(user_input):
            print("❌ Invalid input. Please check your parameters and try again.")
            sys.exit(1)
        
        # Step 3: Display search summary
        display_search_summary(user_input)
        
        # Step 4: Initialize API client
        client = PlacesAPIClient(user_input['api_key'])
        
        # Step 5: Format location string
        location = f"{user_input['latitude']},{user_input['longitude']}"
        
        # Step 6: Search for places
        print("🔍 Searching for places...")
        places_data = client.search_nearby_places(
            location=location,
            keyword=user_input['keyword'],
            radius=user_input['radius']
        )
        
        # Step 7: Display results summary
        display_results_summary(places_data)
        
        # Step 8: Save results to JSON file
        if places_data:
            success = save_results_to_json(places_data, user_input['output_file'])
            if success:
                print(f"💾 Results saved to {user_input['output_file']}")
            else:
                print("❌ Error saving results to file")
                sys.exit(1)
        else:
            print("No results to save.")
        
        print("\n✨ Search completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Search interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()