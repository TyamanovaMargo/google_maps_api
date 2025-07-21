#!/usr/bin/env python3
"""
Google Maps Places API Search - Enhanced Main CLI Script

This script provides a comprehensive command-line interface for searching places using
the Google Maps Places API with full data extraction capabilities.
"""

import sys
import os
from places_api import PlacesAPIClient
from utils import (save_results_to_json, validate_user_input, 
                   create_filtered_json, export_to_csv)

# Try to import from existing config.py, with fallbacks
try:
    from config import GOOGLE_MAPS_API_KEY
except ImportError:
    GOOGLE_MAPS_API_KEY = "YOUR_API_KEY_HERE"

try:
    from config import DEFAULT_SETTINGS
except ImportError:
    DEFAULT_SETTINGS = {
        'radius': '1000',
        'output_file': 'places_results.json'
    }

try:
    from config import EXAMPLE_LOCATIONS
except ImportError:
    EXAMPLE_LOCATIONS = {
        'tel_aviv': {
            'description': 'Тель-Авив центр',
            'latitude': '32.0853',
            'longitude': '34.7818'
        },
        'jerusalem': {
            'description': 'Иерусалим центр', 
            'latitude': '31.7683',
            'longitude': '35.2137'
        },
        'petah_tikva': {
            'description': 'Петах-Тиква центр',
            'latitude': '32.0873',
            'longitude': '34.8876'
        }
    }


def show_example_locations():
    """Display available example locations for quick testing."""
    print("\n📍 Example locations for quick testing:")
    print("-" * 50)
    for key, location in EXAMPLE_LOCATIONS.items():
        print(f"  {key}: {location['description']}")
        print(f"     📍 {location['latitude']}, {location['longitude']}")
    print("-" * 50)


def get_user_input():
    """
    Collect user input for API parameters via command line interface.
    
    Returns:
        dict: Dictionary containing user input parameters
    """
    print("=" * 60)
    print("🗺️  Google Maps Places API Search Tool - Enhanced Edition")
    print("=" * 60)
    print()
    
    # API Key configuration
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
    
    # Location selection
    show_locations = input("\n🌍 Show example locations? (y/n, default: n): ").strip().lower()
    if show_locations in ['y', 'yes']:
        show_example_locations()
        
        use_example = input("\nUse example location? Enter key (or 'n' for custom): ").strip().lower()
        if use_example in EXAMPLE_LOCATIONS:
            location = EXAMPLE_LOCATIONS[use_example]
            latitude = location['latitude']
            longitude = location['longitude']
            print(f"📍 Using {location['description']}: {latitude}, {longitude}")
        else:
            print("📍 Enter custom coordinates:")
            latitude = input("Latitude: ").strip()
            longitude = input("Longitude: ").strip()
    else:
        print("\n📍 Enter location coordinates:")
        latitude = input("Latitude: ").strip()
        longitude = input("Longitude: ").strip()
    
    # Search parameters
    keyword = input("\n🔍 Enter search keyword (e.g., 'restaurant', 'hospital', 'cafe'): ").strip()
    
    # Radius with default value
    default_radius = DEFAULT_SETTINGS.get('radius', '1000')
    radius = input(f"📏 Enter search radius in meters (1-50000, default: {default_radius}): ").strip()
    if not radius:
        radius = default_radius
    
    # Output options
    print("\n💾 Output Options:")
    default_filename = DEFAULT_SETTINGS.get('output_file', 'places_results.json')
    output_file = input(f"JSON filename (default: {default_filename}): ").strip()
    if not output_file:
        output_file = default_filename
    
    # Additional export options
    export_csv = input("Also export to CSV? (y/n, default: n): ").strip().lower() in ['y', 'yes']
    create_minimal = input("Create minimal JSON with basic info only? (y/n, default: n): ").strip().lower() in ['y', 'yes']
    
    return {
        'api_key': api_key,
        'latitude': latitude,
        'longitude': longitude,
        'keyword': keyword,
        'radius': radius,
        'output_file': output_file,
        'export_csv': export_csv,
        'create_minimal': create_minimal
    }


def display_search_summary(user_input):
    """Display a summary of the search parameters before starting."""
    print("\n" + "="*50)
    print("🔍 SEARCH CONFIGURATION")
    print("="*50)
    print(f"📍 Location: {user_input['latitude']}, {user_input['longitude']}")
    print(f"🏷️  Keyword: {user_input['keyword']}")
    print(f"📏 Radius: {user_input['radius']} meters")
    print(f"💾 Main output: {user_input['output_file']}")
    if user_input['export_csv']:
        csv_name = user_input['output_file'].replace('.json', '.csv')
        print(f"📊 CSV export: {csv_name}")
    if user_input['create_minimal']:
        minimal_name = user_input['output_file'].replace('.json', '_minimal.json')
        print(f"📋 Minimal JSON: {minimal_name}")
    print("="*50)
    print()


def display_results_summary(places_data):
    """Display a comprehensive summary of the search results."""
    if not places_data:
        print("❌ No places found matching your criteria.")
        return
    
    print(f"\n✅ Successfully found {len(places_data)} places!")
    print("\n📊 Quick Statistics:")
    
    # Count places with different data types
    with_ratings = sum(1 for p in places_data if p.get('rating'))
    with_phone = sum(1 for p in places_data if p.get('formatted_phone_number'))
    with_website = sum(1 for p in places_data if p.get('website'))
    with_reviews = sum(1 for p in places_data if p.get('reviews'))
    
    print(f"   ⭐ Places with ratings: {with_ratings}")
    print(f"   📞 Places with phone numbers: {with_phone}")
    print(f"   🌐 Places with websites: {with_website}")
    print(f"   📝 Places with reviews: {with_reviews}")
    
    # Show preview of top results
    print(f"\n🏆 Top {min(5, len(places_data))} Results:")
    print("-" * 60)
    
    for i, place in enumerate(places_data[:5], 1):
        print(f"{i}. 🏢 {place.get('name', 'Unknown')}")
        print(f"   📍 {place.get('formatted_address', 'No address')}")
        print(f"   🌐 {place.get('latitude', 'N/A')}, {place.get('longitude', 'N/A')}")
        
def display_results_summary(places_data):
    """Display a comprehensive summary of the search results."""
    if not places_data:
        print("❌ No places found matching your criteria.")
        return
    
    print(f"\n✅ Successfully found {len(places_data)} places!")
    print("\n📊 Quick Statistics:")
    
    # Count places with different data types
    with_ratings = sum(1 for p in places_data if p.get('rating'))
    with_phone = sum(1 for p in places_data if p.get('formatted_phone_number'))
    with_website = sum(1 for p in places_data if p.get('website'))
    with_reviews = sum(1 for p in places_data if p.get('reviews'))
    
    print(f"   ⭐ Places with ratings: {with_ratings}")
    print(f"   📞 Places with phone numbers: {with_phone}")
    print(f"   🌐 Places with websites: {with_website}")
    print(f"   📝 Places with reviews: {with_reviews}")
    
    # Show preview of top results
    print(f"\n🏆 Top {min(5, len(places_data))} Results:")
    print("-" * 60)
    
    for i, place in enumerate(places_data[:5], 1):
        print(f"{i}. 🏢 {place.get('name', 'Unknown')}")
        print(f"   📍 {place.get('formatted_address', 'No address')}")
        print(f"   🌐 {place.get('latitude', 'N/A')}, {place.get('longitude', 'N/A')}")
        
        rating = place.get('rating')
        if rating:
            stars = "⭐" * int(rating)
            print(f"   {stars} {rating}/5 ({place.get('user_ratings_total', 0)} reviews)")
        
        if place.get('website'):
            print(f"   🌐 {place['website']}")
        if place.get('formatted_phone_number'):
            print(f"   📞 {place['formatted_phone_number']}")
        
        print()
    
    if len(places_data) > 5:
        print(f"   ... and {len(places_data) - 5} more places")


def save_all_formats(places_data, user_input):
    """Save results in all requested formats."""
    saved_files = []
    
    # Main JSON file with full data
    print(f"💾 Saving main data to {user_input['output_file']}...")
    if save_results_to_json(places_data, user_input['output_file']):
        saved_files.append(user_input['output_file'])
    else:
        print("❌ Error saving main JSON file")
        return False
    
    # CSV export if requested
    if user_input['export_csv']:
        csv_filename = user_input['output_file'].replace('.json', '.csv')
        print(f"📊 Exporting to CSV: {csv_filename}...")
        if export_to_csv(places_data, csv_filename):
            saved_files.append(csv_filename)
    
    # Minimal JSON if requested
    if user_input['create_minimal']:
        minimal_filename = user_input['output_file'].replace('.json', '_minimal.json')
        minimal_fields = ['name', 'formatted_address', 'latitude', 'longitude', 
                         'rating', 'formatted_phone_number', 'website', 'types']
        print(f"📋 Creating minimal JSON: {minimal_filename}...")
        if create_filtered_json(places_data, minimal_filename, minimal_fields):
            saved_files.append(minimal_filename)
    
    # Display saved files
    if saved_files:
        print(f"\n✅ Files saved: {len(saved_files)}")
        for filename in saved_files:
            file_size = os.path.getsize(filename)
            if file_size > 1024 * 1024:
                size_str = f"{file_size / (1024 * 1024):.2f} MB"
            else:
                size_str = f"{file_size / 1024:.2f} KB"
            print(f"   📁 {filename} ({size_str})")
        return True
    
    return False


def main():
    """Main function that orchestrates the entire search process."""
    try:
        print("🚀 Starting enhanced places search...")
        
        # Step 1: Get user input
        user_input = get_user_input()
        
        # Step 2: Validate input
        print("\n🔍 Validating input parameters...")
        if not validate_user_input(user_input):
            print("❌ Invalid input. Please check your parameters and try again.")
            sys.exit(1)
        
        # Step 3: Display search summary
        display_search_summary(user_input)
        
        # Confirmation
        proceed = input("Continue with search? (y/n, default: y): ").strip().lower()
        if proceed in ['n', 'no']:
            print("🛑 Search cancelled by user")
            sys.exit(0)
        
        # Step 4: Initialize API client
        print("🔧 Initializing API client...")
        client = PlacesAPIClient(user_input['api_key'])
        
        # Step 5: Format location string
        location = f"{user_input['latitude']},{user_input['longitude']}"
        
        # Step 6: Search for places
        print(f"🔍 Searching for places with keyword '{user_input['keyword']}'...")
        print("⏳ This may take a while as we're collecting comprehensive information...")
        
        places_data = client.search_nearby_places(
            location=location,
            keyword=user_input['keyword'],
            radius=user_input['radius']
        )
        
        # Step 7: Display results summary
        display_results_summary(places_data)
        
        # Step 8: Save results in all requested formats
        if places_data:
            if save_all_formats(places_data, user_input):
                print("\n🎉 Search completed successfully!")
                
                # Display data richness info
                total_reviews = sum(len(p.get('reviews', [])) for p in places_data)
                total_photos = sum(len(p.get('photos', [])) for p in places_data)
                print(f"📊 Additional data collected:")
                print(f"   📝 {total_reviews} reviews")
                print(f"   📸 {total_photos} photo references")
                
            else:
                print("❌ Error saving results")
                sys.exit(1)
        else:
            print("ℹ️  No results to save.")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Search interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()