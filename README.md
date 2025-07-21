# Google Maps Places API Search

A Python project for searching places and businesses around a given location using the Google Maps Places API.

## 📋 Project Description

This project provides a command-line interface to search for places using Google's Places API. It can find restaurants, hospitals, shops, and any other businesses within a specified radius of given coordinates. The results are saved as JSON files for further processing or analysis.

### Features

- ✅ Search places by keyword around any location
- ✅ Configurable search radius (1-50,000 meters)
- ✅ Automatic pagination handling (up to 60 results)
- ✅ Comprehensive error handling
- ✅ JSON output with metadata
- ✅ Input validation and user-friendly CLI
- ✅ Modular code structure

## 🚀 Setup Instructions

### Prerequisites

- Python 3.7 or higher
- Google Maps API Key with Places API enabled

### Installation

1. **Clone or download this project**
   ```bash
   git clone <repository-url>
   cd google-maps-places-search
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get Google Maps API Key**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the "Places API"
   - Create credentials (API Key)
   - (Optional) Restrict the API key to Places API for security

### Project Structure

```
google-maps-places-search/
├── main.py              # Main CLI script
├── places_api.py        # Google Places API client
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🖥️ Usage

### Basic Usage

Run the main script and follow the interactive prompts:

```bash
python main.py
```

The script will ask for:
- **API Key**: Your Google Maps API key
- **Latitude**: Location latitude (e.g., `40.7128` for NYC)
- **Longitude**: Location longitude (e.g., `-74.0060` for NYC)
- **Keyword**: Search term (e.g., `restaurant`, `hospital`, `coffee`)
- **Radius**: Search radius in meters (1-50000)
- **Output File**: JSON filename (optional, defaults to `places_results.json`)

### Example Session

```
==================================================
Google Maps Places API Search Tool
==================================================

Enter your Google Maps API Key: AIzaSyC...
Enter location coordinates:
Latitude: 40.7128
Longitude: -74.0060

Enter search keyword (e.g., 'restaurant', 'hospital', 'cafe'): pizza
Enter search radius in meters (1-50000): 2000
Enter output filename (press Enter for 'places_results.json'): nyc_pizza.json

----------------------------------------
SEARCH SUMMARY
----------------------------------------
Location: 40.7128, -74.0060
Keyword: pizza
Radius: 2000 meters
Output file: nyc_pizza.json
----------------------------------------

🔍 Starting search for 'pizza' near 40.7128,-74.0060 within 2000m radius
📡 Making API request...
📄 Page 1: Found 20 places
⏳ Waiting for next page token to become valid...
📡 Making API request... (page token: CmRaAAAA2b...)
📄 Page 2: Found 20 places
✅ Search completed. Total places found: 40

✅ Found 40 places!

First 5 results:
----------------------------------------
1. Joe's Pizza
   📍 7 Carmine St, New York
   🌐 40.7301, -74.0027

2. Prince Street Pizza
   📍 27 Prince St, New York
   🌐 40.7229, -74.0027

... and 35 more places

💾 Results saved to nyc_pizza.json
✅ Successfully saved 40 places to nyc_pizza.json

✨ Search completed successfully!
```

## 📊 Example Output Format

The results are saved as JSON with the following structure:

```json
{
  "metadata": {
    "search_timestamp": "2025-01-15T10:30:00.123456",
    "total_places": 25,
    "file_version": "1.0"
  },
  "places": [
    {
      "name": "Joe's Pizza",
      "address": "7 Carmine St, New York",
      "latitude": 40.7301,
      "longitude": -74.0027
    },
    {
      "name": "Prince Street Pizza",
      "address": "27 Prince St, New York", 
      "latitude": 40.7229,
      "longitude": -74.0027
    },
    {
      "name": "Di Fara Pizza",
      "address": "424 E 9th St, New York",
      "latitude": 40.7267,
      "longitude": -73.9821
    }
  ]
}
```

## 🔧 Module Documentation

### `main.py`
- Main CLI script that orchestrates the search process
- Handles user input collection and validation
- Displays search progress and results summary

### `places_api.py`
- `PlacesAPIClient`: Main API client class
- `search_nearby_places()`: Search with pagination support
- `_make_api_request()`: Handle individual API requests
- `_extract_place_data()`: Parse API responses

### `utils.py`
- `validate_user_input()`: Validate all user inputs
- `save_results_to_json()`: Save results with metadata
- `load_results_from_json()`: Load previously saved results
- Various helper functions for formatting and calculations

## 📝 API Limits & Notes

- **Results per page**: 20 (Google limit)
- **Maximum pages**: 3 (60 total results maximum)
- **Radius limit**: 50,000 meters (Google limit)
- **Rate limits**: Depends on your Google API plan
- **Required API**: Google Places API (Nearby Search)

## ❌ Error Handling

The project handles various error scenarios:

- Invalid API keys
- Network connectivity issues
- Malformed API responses
- Invalid coordinate ranges
- File permission errors
- API quota exceeded
- Timeout errors

## 🛠️ Troubleshooting

### Common Issues

1. **"API key invalid"**
   - Verify your API key is correct
   - Ensure Places API is enabled in Google Cloud Console
   - Check API key restrictions

2. **"No results found"**
   - Try a different keyword
   - Increase the search radius
   - Verify coordinates are correct