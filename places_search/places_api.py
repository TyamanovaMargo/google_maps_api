#!/usr/bin/env python3
"""
Google Maps Places API Client - Enhanced Version

This module provides functionality to interact with the Google Maps Places API
and extract comprehensive information about places.
"""

import requests
import json
from typing import List, Dict, Optional


class PlacesAPIClient:
    """
    Client for interacting with Google Maps Places API with enhanced data extraction.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the Places API client.
        
        Args:
            api_key (str): Google Maps API key
        """
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place"
    
    def search_nearby_places(self, location: str, keyword: str, radius: str = "1000") -> List[Dict]:
        """
        Search for places near a location with comprehensive data extraction.
        
        Args:
            location (str): Latitude,longitude string
            keyword (str): Search keyword
            radius (str): Search radius in meters
            
        Returns:
            List[Dict]: List of places with comprehensive information
        """
        # Step 1: Get basic place data from Nearby Search
        nearby_url = f"{self.base_url}/nearbysearch/json"
        nearby_params = {
            'location': location,
            'radius': radius,
            'keyword': keyword,
            'key': self.api_key
        }
        
        print(f"🔍 Searching for places near {location}...")
        response = requests.get(nearby_url, params=nearby_params)
        
        if response.status_code != 200:
            print(f"❌ API request failed with status {response.status_code}")
            return []
        
        data = response.json()
        
        if data.get('status') != 'OK':
            print(f"❌ API returned status: {data.get('status')}")
            if 'error_message' in data:
                print(f"Error message: {data['error_message']}")
            return []
        
        places = data.get('results', [])
        print(f"📍 Found {len(places)} places, getting detailed information...")
        
        # Step 2: Get detailed information for each place
        detailed_places = []
        for i, place in enumerate(places, 1):
            print(f"📋 Processing place {i}/{len(places)}: {place.get('name', 'Unknown')}")
            detailed_place = self._get_place_details(place)
            if detailed_place:
                detailed_places.append(detailed_place)
        
        return detailed_places
    
    def _get_place_details(self, place: Dict) -> Optional[Dict]:
        """
        Get detailed information for a specific place.
        
        Args:
            place (Dict): Basic place data from Nearby Search
            
        Returns:
            Optional[Dict]: Detailed place information or None if failed
        """
        place_id = place.get('place_id')
        if not place_id:
            return self._extract_basic_info(place)
        
        # Get detailed place information
        details_url = f"{self.base_url}/details/json"
        details_params = {
            'place_id': place_id,
            'fields': ','.join([
                'place_id', 'name', 'formatted_address', 'vicinity',
                'geometry', 'types', 'business_status', 'price_level',
                'rating', 'user_ratings_total', 'reviews',
                'formatted_phone_number', 'international_phone_number',
                'website', 'url', 'opening_hours', 'photos',
                'plus_code', 'permanently_closed', 'editorial_summary',
                'delivery', 'dine_in', 'takeout', 'reservable',
                'serves_breakfast', 'serves_lunch', 'serves_dinner',
                'serves_beer', 'serves_wine', 'serves_brunch',
                'wheelchair_accessible_entrance', 'curbside_pickup'
            ]),
            'key': self.api_key
        }
        
        try:
            response = requests.get(details_url, params=details_params)
            if response.status_code == 200:
                details_data = response.json()
                if details_data.get('status') == 'OK':
                    detailed_place = details_data.get('result', {})
                    return self._extract_comprehensive_info(place, detailed_place)
        except Exception as e:
            print(f"⚠️ Error getting details for {place.get('name', 'Unknown')}: {e}")
        
        # Fallback to basic info if details request fails
        return self._extract_basic_info(place)
    
    def _extract_comprehensive_info(self, basic_place: Dict, detailed_place: Dict) -> Dict:
        """
        Extract comprehensive information from both basic and detailed place data.
        
        Args:
            basic_place (Dict): Basic place data from Nearby Search
            detailed_place (Dict): Detailed place data from Place Details
            
        Returns:
            Dict: Comprehensive place information
        """
        # Get geometry information
        geometry = detailed_place.get('geometry') or basic_place.get('geometry', {})
        location = geometry.get('location', {})
        
        # Extract photos information
        photos = []
        if detailed_place.get('photos'):
            for photo in detailed_place['photos'][:5]:  # Limit to first 5 photos
                photo_info = {
                    'photo_reference': photo.get('photo_reference'),
                    'width': photo.get('width'),
                    'height': photo.get('height'),
                    'html_attributions': photo.get('html_attributions', []),
                    'photo_url': f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo.get('photo_reference')}&key={self.api_key}" if photo.get('photo_reference') else None
                }
                photos.append(photo_info)
        
        # Extract reviews
        reviews = []
        if detailed_place.get('reviews'):
            for review in detailed_place['reviews']:
                review_info = {
                    'author_name': review.get('author_name'),
                    'author_url': review.get('author_url'),
                    'language': review.get('language'),
                    'profile_photo_url': review.get('profile_photo_url'),
                    'rating': review.get('rating'),
                    'relative_time_description': review.get('relative_time_description'),
                    'text': review.get('text'),
                    'time': review.get('time')
                }
                reviews.append(review_info)
        
        # Extract opening hours
        opening_hours = {}
        if detailed_place.get('opening_hours'):
            oh = detailed_place['opening_hours']
            opening_hours = {
                'open_now': oh.get('open_now'),
                'weekday_text': oh.get('weekday_text', []),
                'periods': oh.get('periods', [])
            }
        
        # Build comprehensive place data
        place_data = {
            # Basic identification
            'place_id': detailed_place.get('place_id') or basic_place.get('place_id'),
            'name': detailed_place.get('name') or basic_place.get('name'),
            'types': detailed_place.get('types') or basic_place.get('types', []),
            
            # Location information
            'latitude': location.get('lat'),
            'longitude': location.get('lng'),
            'formatted_address': detailed_place.get('formatted_address') or basic_place.get('vicinity'),
            'vicinity': detailed_place.get('vicinity') or basic_place.get('vicinity'),
            'plus_code': detailed_place.get('plus_code', {}),
            
            # Business information
            'business_status': detailed_place.get('business_status') or basic_place.get('business_status'),
            'permanently_closed': detailed_place.get('permanently_closed', False),
            'price_level': detailed_place.get('price_level') or basic_place.get('price_level'),
            
            # Ratings and reviews
            'rating': detailed_place.get('rating') or basic_place.get('rating'),
            'user_ratings_total': detailed_place.get('user_ratings_total') or basic_place.get('user_ratings_total'),
            'reviews': reviews,
            
            # Contact information
            'formatted_phone_number': detailed_place.get('formatted_phone_number'),
            'international_phone_number': detailed_place.get('international_phone_number'),
            'website': detailed_place.get('website'),
            'url': detailed_place.get('url'),
            
            # Operating hours
            'opening_hours': opening_hours,
            
            # Photos
            'photos': photos,
            
            # Services and amenities
            'delivery': detailed_place.get('delivery'),
            'dine_in': detailed_place.get('dine_in'),
            'takeout': detailed_place.get('takeout'),
            'reservable': detailed_place.get('reservable'),
            'serves_breakfast': detailed_place.get('serves_breakfast'),
            'serves_lunch': detailed_place.get('serves_lunch'),
            'serves_dinner': detailed_place.get('serves_dinner'),
            'serves_beer': detailed_place.get('serves_beer'),
            'serves_wine': detailed_place.get('serves_wine'),
            'serves_brunch': detailed_place.get('serves_brunch'),
            'wheelchair_accessible_entrance': detailed_place.get('wheelchair_accessible_entrance'),
            'curbside_pickup': detailed_place.get('curbside_pickup'),
            
            # Additional information
            'editorial_summary': detailed_place.get('editorial_summary', {}),
            'geometry': geometry,
            
            # Raw data (for debugging or future use)
            'raw_basic_data': basic_place,
            'raw_detailed_data': detailed_place
        }
        
        return place_data
    
    def _extract_basic_info(self, place: Dict) -> Dict:
        """
        Extract basic information when detailed data is not available.
        
        Args:
            place (Dict): Basic place data
            
        Returns:
            Dict: Basic place information
        """
        geometry = place.get('geometry', {})
        location = geometry.get('location', {})
        
        # Extract basic photos
        photos = []
        if place.get('photos'):
            for photo in place['photos'][:3]:  # Limit to first 3 photos for basic
                photo_info = {
                    'photo_reference': photo.get('photo_reference'),
                    'width': photo.get('width'),
                    'height': photo.get('height'),
                    'photo_url': f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo.get('photo_reference')}&key={self.api_key}" if photo.get('photo_reference') else None
                }
                photos.append(photo_info)
        
        return {
            # Basic identification
            'place_id': place.get('place_id'),
            'name': place.get('name'),
            'types': place.get('types', []),
            
            # Location information
            'latitude': location.get('lat'),
            'longitude': location.get('lng'),
            'formatted_address': place.get('vicinity'),
            'vicinity': place.get('vicinity'),
            
            # Business information
            'business_status': place.get('business_status'),
            'permanently_closed': place.get('permanently_closed', False),
            'price_level': place.get('price_level'),
            
            # Ratings
            'rating': place.get('rating'),
            'user_ratings_total': place.get('user_ratings_total'),
            
            # Basic photos
            'photos': photos,
            
            # Geometry
            'geometry': geometry,
            
            # Raw data
            'raw_basic_data': place,
            'raw_detailed_data': None
        }