#!/usr/bin/env python3
"""
Utility Functions - Enhanced Version

This module provides utility functions for validation, data processing,
and file operations with enhanced JSON output formatting.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any


def validate_user_input(user_input: Dict[str, str]) -> bool:
    """
    Validate user input parameters.
    
    Args:
        user_input (dict): Dictionary containing user input
        
    Returns:
        bool: True if all inputs are valid, False otherwise
    """
    try:
        # Validate API key
        if not user_input.get('api_key') or user_input['api_key'].strip() == '':
            print("❌ API key is required")
            return False
        
        # Validate latitude
        lat = float(user_input['latitude'])
        if not -90 <= lat <= 90:
            print("❌ Latitude must be between -90 and 90")
            return False
        
        # Validate longitude
        lng = float(user_input['longitude'])
        if not -180 <= lng <= 180:
            print("❌ Longitude must be between -180 and 180")
            return False
        
        # Validate keyword
        if not user_input.get('keyword') or user_input['keyword'].strip() == '':
            print("❌ Search keyword is required")
            return False
        
        # Validate radius
        radius = int(user_input['radius'])
        if not 1 <= radius <= 50000:
            print("❌ Radius must be between 1 and 50000 meters")
            return False
        
        # Validate output filename
        if not user_input.get('output_file') or user_input['output_file'].strip() == '':
            print("❌ Output filename is required")
            return False
        
        return True
        
    except ValueError as e:
        print(f"❌ Invalid input format: {e}")
        return False
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False


def save_results_to_json(places_data: List[Dict], filename: str, include_metadata: bool = True) -> bool:
    """
    Save search results to a JSON file with comprehensive formatting and metadata.
    
    Args:
        places_data (List[Dict]): List of place dictionaries
        filename (str): Output filename
        include_metadata (bool): Whether to include search metadata
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Prepare the output structure
        output_data = {}
        
        if include_metadata:
            # Add metadata
            output_data['metadata'] = {
                'search_timestamp': datetime.now().isoformat(),
                'total_places_found': len(places_data),
                'api_used': 'Google Maps Places API',
                'data_structure_version': '2.0'
            }
        
        # Add places data
        output_data['places'] = places_data
        
        # Create summary statistics
        if include_metadata and places_data:
            output_data['summary'] = generate_summary_stats(places_data)
        
        # Write to file with pretty formatting
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False, default=json_serializer)
        
        print(f"📊 Saved {len(places_data)} places to {filename}")
        
        # Display file size
        file_size = os.path.getsize(filename)
        size_mb = file_size / (1024 * 1024)
        if size_mb > 1:
            print(f"📁 File size: {size_mb:.2f} MB")
        else:
            print(f"📁 File size: {file_size / 1024:.2f} KB")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving to JSON file: {e}")
        return False


def generate_summary_stats(places_data: List[Dict]) -> Dict[str, Any]:
    """
    Generate summary statistics from places data.
    
    Args:
        places_data (List[Dict]): List of place dictionaries
        
    Returns:
        Dict[str, Any]: Summary statistics
    """
    if not places_data:
        return {}
    
    # Count places by type
    type_counts = {}
    ratings = []
    price_levels = []
    business_statuses = []
    has_phone = 0
    has_website = 0
    has_reviews = 0
    total_reviews = 0
    
    for place in places_data:
        # Count types
        for place_type in place.get('types', []):
            type_counts[place_type] = type_counts.get(place_type, 0) + 1
        
        # Collect ratings
        if place.get('rating'):
            ratings.append(place['rating'])
        
        # Collect price levels
        if place.get('price_level') is not None:
            price_levels.append(place['price_level'])
        
        # Count business statuses
        status = place.get('business_status', 'UNKNOWN')
        business_statuses.append(status)
        
        # Count places with contact info
        if place.get('formatted_phone_number'):
            has_phone += 1
        if place.get('website'):
            has_website += 1
        
        # Count reviews
        reviews = place.get('reviews', [])
        if reviews:
            has_reviews += 1
            total_reviews += len(reviews)
    
    # Calculate statistics
    summary = {
        'total_places': len(places_data),
        'place_types': {
            'most_common_types': sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            'unique_types_count': len(type_counts)
        },
        'ratings': {
            'places_with_ratings': len(ratings),
            'average_rating': round(sum(ratings) / len(ratings), 2) if ratings else None,
            'highest_rating': max(ratings) if ratings else None,
            'lowest_rating': min(ratings) if ratings else None
        },
        'price_levels': {
            'places_with_price_info': len(price_levels),
            'price_distribution': {
                'free (0)': price_levels.count(0),
                'inexpensive (1)': price_levels.count(1),
                'moderate (2)': price_levels.count(2),
                'expensive (3)': price_levels.count(3),
                'very_expensive (4)': price_levels.count(4)
            }
        },
        'business_status': {
            'operational': business_statuses.count('OPERATIONAL'),
            'closed_temporarily': business_statuses.count('CLOSED_TEMPORARILY'),
            'closed_permanently': business_statuses.count('CLOSED_PERMANENTLY'),
            'unknown': business_statuses.count('UNKNOWN')
        },
        'contact_information': {
            'places_with_phone': has_phone,
            'places_with_website': has_website,
            'phone_coverage_percent': round((has_phone / len(places_data)) * 100, 1),
            'website_coverage_percent': round((has_website / len(places_data)) * 100, 1)
        },
        'reviews': {
            'places_with_reviews': has_reviews,
            'total_reviews_collected': total_reviews,
            'average_reviews_per_place': round(total_reviews / has_reviews, 1) if has_reviews else 0
        }
    }
    
    return summary


def json_serializer(obj):
    """
    Custom JSON serializer for handling special data types.
    
    Args:
        obj: Object to serialize
        
    Returns:
        Serializable representation of the object
    """
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def create_filtered_json(places_data: List[Dict], filename: str, fields: List[str]) -> bool:
    """
    Create a filtered JSON file with only specified fields.
    
    Args:
        places_data (List[Dict]): List of place dictionaries
        filename (str): Output filename
        fields (List[str]): List of fields to include
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        filtered_places = []
        for place in places_data:
            filtered_place = {}
            for field in fields:
                if field in place:
                    filtered_place[field] = place[field]
            filtered_places.append(filtered_place)
        
        return save_results_to_json(filtered_places, filename, include_metadata=False)
        
    except Exception as e:
        print(f"❌ Error creating filtered JSON: {e}")
        return False


def export_to_csv(places_data: List[Dict], filename: str) -> bool:
    """
    Export basic place information to CSV format.
    
    Args:
        places_data (List[Dict]): List of place dictionaries
        filename (str): Output filename (should end with .csv)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import csv
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        # Define basic fields for CSV export
        fields = [
            'name', 'formatted_address', 'latitude', 'longitude',
            'rating', 'user_ratings_total', 'price_level', 'business_status',
            'formatted_phone_number', 'website', 'types'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            
            for place in places_data:
                row = {}
                for field in fields:
                    value = place.get(field)
                    if field == 'types' and isinstance(value, list):
                        row[field] = ', '.join(value)
                    else:
                        row[field] = value
                writer.writerow(row)
        
        print(f"📊 Exported {len(places_data)} places to {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error exporting to CSV: {e}")
        return False