"""
Google Maps Places API Client

This module provides a client class for interacting with the Google Maps Places API.
It handles API requests, pagination, error handling, and data extraction.
"""

import requests
import time
from typing import List, Dict, Optional


class PlacesAPIClient:
    """
    A client for interacting with Google Maps Places API.
    
    This class handles authentication, API requests, pagination,
    and error handling for the Google Places Nearby Search API.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the Places API client.
        
        Args:
            api_key (str): Google Maps API key
        """
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    def _make_api_request(self, location: str, keyword: str, radius: str, page_token: Optional[str] = None) -> Dict:
        """
        Make a single request to the Google Maps Places API.
        
        Args:
            location (str): Latitude,longitude coordinates (e.g., "40.7128,-74.0060")
            keyword (str): Search keyword (e.g., "restaurant", "hospital")
            radius (str): Search radius in meters
            page_token (str, optional): Token for pagination
        
        Returns:
            dict: API response as dictionary
        
        Raises:
            requests.RequestException: If the API request fails
        """
        # Build request parameters
        params = {
            'location': location,
            'radius': radius,
            'keyword': keyword,
            'key': self.api_key
        }
        
        # Add page token for pagination if provided
        if page_token:
            params['pagetoken'] = page_token
        
        try:
            print(f"📡 Making API request..." + (f" (page token: {page_token[:20]}...)" if page_token else ""))
            
            # Send GET request to Google Places API
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Parse JSON response
            json_response = response.json()
            
            # Check API-specific status
            if json_response.get('status') not in ['OK', 'ZERO_RESULTS']:
                error_msg = json_response.get('error_message', f"API returned status: {json_response.get('status')}")
                raise requests.RequestException(f"Google Places API error: {error_msg}")
            
            return json_response
            
        except requests.exceptions.Timeout:
            raise requests.RequestException("Request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"API request failed: {str(e)}")
        except ValueError as e:
            raise requests.RequestException(f"Invalid JSON response: {str(e)}")
    
    def _extract_place_data(self, api_response: Dict) -> List[Dict]:
        """
        Extract relevant place data from Google Places API response.
        
        Args:
            api_response (dict): Raw API response
        
        Returns:
            list: List of dictionaries containing extracted place data
        """
        places = []
        
        # Check if response contains results
        if 'results' not in api_response or not api_response['results']:
            return places
        
        # Extract data for each place
        for place in api_response['results']:
            # Get basic place information
            place_data = {
                'name': place.get('name', 'Unknown'),
                'address': place.get('vicinity', 'Address not available'),
                'latitude': None,
                'longitude': None
            }
            
            # Extract coordinates from geometry
            geometry = place.get('geometry', {})
            location = geometry.get('location', {})
            
            if location:
                place_data['latitude'] = location.get('lat')
                place_data['longitude'] = location.get('lng')
            
            # Only add places with valid coordinates
            if place_data['latitude'] is not None and place_data['longitude'] is not None:
                places.append(place_data)
        
        return places
    
    def search_nearby_places(self, location: str, keyword: str, radius: str) -> List[Dict]:
        """
        Search for nearby places using Google Places API with pagination support.
        
        This method handles multiple API requests to fetch all available results,
        as Google Places API returns maximum 20 results per request with up to
        3 pages (60 total results).
        
        Args:
            location (str): Latitude,longitude coordinates
            keyword (str): Search keyword
            radius (str): Search radius in meters
        
        Returns:
            list: Complete list of places found across all pages
        
        Raises:
            requests.RequestException: If API requests fail
        """
        all_places = []
        next_page_token = None
        page_count = 0
        max_pages = 3  # Google Places API maximum pages
        
        print(f"🔍 Starting search for '{keyword}' near {location} within {radius}m radius")
        
        while page_count < max_pages:
            try:
                # Make API request
                response = self._make_api_request(location, keyword, radius, next_page_token)
                
                # Handle zero results
                if response.get('status') == 'ZERO_RESULTS':
                    if page_count == 0:
                        print("ℹ️ No places found matching your criteria")
                    break
                
                # Extract place data from current page
                places_data = self._extract_place_data(response)
                all_places.extend(places_data)
                
                page_count += 1
                print(f"📄 Page {page_count}: Found {len(places_data)} places")
                
                # Check for next page
                next_page_token = response.get('next_page_token')
                if not next_page_token:
                    print("ℹ️ No more pages available")
                    break
                
                # Google requires a delay before using next page token
                if page_count < max_pages:
                    print("⏳ Waiting for next page token to become valid...")
                    time.sleep(3)  # Wait 3 seconds for token to become valid
                
            except requests.RequestException as e:
                print(f"❌ Error on page {page_count + 1}: {e}")
                # Continue with results we have so far
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                break
        
        print(f"✅ Search completed. Total places found: {len(all_places)}")
        return all_places
    
    def get_place_details(self, place_id: str) -> Dict:
        """
        Get detailed information for a specific place.
        
        Note: This method is not used in the main search functionality
        but is provided for potential future enhancements.
        
        Args:
            place_id (str): Google Places place_id
        
        Returns:
            dict: Detailed place information
        """
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        
        params = {
            'place_id': place_id,
            'key': self.api_key,
            'fields': 'name,formatted_address,geometry,rating,reviews'
        }
        
        try:
            response = requests.get(details_url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to get place details: {str(e)}")
    
    def validate_api_key(self) -> bool:
        """
        Validate if the API key is working by making a simple test request.
        
        Returns:
            bool: True if API key is valid, False otherwise
        """
        test_params = {
            'location': '37.7749,-122.4194',  # San Francisco coordinates
            'radius': '1000',
            'keyword': 'test',
            'key': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=test_params, timeout=10)
            json_response = response.json()
            
            # Check if we get a valid response (OK or ZERO_RESULTS are both valid)
            return json_response.get('status') in ['OK', 'ZERO_RESULTS']
            
        except Exception:
            return False