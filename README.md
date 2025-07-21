# Google Maps Places API Search

A Python project for searching places and businesses around a given location using the Google Maps Places API.

## 📋 Project Description

This project provides a command-line interface to search for places using Google's Places API. It can find restaurants, hospitals, shops, and any other businesses within a specified radius of given coordinates. The results are saved as JSON files for further processing or analysis.

The script will now collect ALL available information about places including:

📝 Full reviews with author details
📸 Photo URLs for download
⏰ Operating hours and schedules
📞 Contact information
🏷️ Services and amenities
💰 Price levels
⭐ Ratings and review count
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

3. **Configure API Key**
   ```bash
   # Copy the example config file
   cp config.example.py config.py
   
   # Edit config.py and add your API key
   # Replace "YOUR_API_KEY_HERE" with your actual Google Maps API key
   ```

4. **Get Google Maps API Key**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the "Places API"
   - Create credentials (API Key)
   - Copy the API key to `config.py`
   - (Optional) Restrict the API key to Places API for security

### Project Structure

```
google-maps-places-search/
├── main.py              # Main CLI script
├── places_api.py        # Google Places API client
├── utils.py             # Utility functions
├── config.py            # Your API configuration (create from example)
├── config.example.py    # Configuration template
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore file (excludes config.py)
└── README.md           # This file
```

## 🖥️ Usage

### Basic Usage

1. **First setup your API key:**
   ```bash
   cp config.example.py config.py
   # Edit config.py and replace YOUR_API_KEY_HERE with your actual API key
   ```

2. **Run the main script:**
   ```bash
   python main.py
   ```

The script will:
- Use the API key from `config.py` (or ask for it if not configured)
- Offer example locations for quick testing
- Ask for search parameters
- Save results to JSON file

### Example Session

```
==================================================
Google Maps Places API Search Tool
==================================================

✅ Using API key from config.py
Use configured API key? (y/n, default: y): y

Show example locations? (y/n, default: n): y

📍 Example locations for quick testing:
----------------------------------------
new_york: New York City, USA (40.7128, -74.0060)
london: London, UK (51.5074, -0.1278)
tokyo: Tokyo, Japan (35.6762, 139.6503)
paris: Paris, France (48.8566, 2.3522)
----------------------------------------

Use example location? Enter key (or 'n' for custom): new_york
Using New York City, USA: 40.7128, -74.0060

Enter search keyword (e.g., 'restaurant', 'hospital', 'cafe'): pizza
Enter search radius in meters (1-50000, default: 1000): 2000
Enter output filename (default: places_results.json): nyc_pizza.json
```

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

### `utils.py`
- `validate_user_input()`: Validate all user inputs
- `save_results_to_json()`: Save results with metadata
- `load_results_from_json()`: Load previously saved results
- Various helper functions for formatting and calculations

## 🛠️ Configuration

### API Key Setup

1. **Create config.py from template:**
   ```bash
   cp config.example.py config.py
   ```

2. **Edit config.py:**
   ```python
   # Replace this line:
   GOOGLE_MAPS_API_KEY = "YOUR_API_KEY_HERE"
   
   # With your actual API key:
   GOOGLE_MAPS_API_KEY = "AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   ```

3. **Security Note:**
   - `config.py` is included in `.gitignore` to prevent accidental commits
   - Never share your API key publicly
   - Consider using environment variables for production deployments

### Default Settings

You can customize default values in `config.py`:

```python
DEFAULT_SETTINGS = {
    "radius": "2000",  # Default search radius
    "output_file": "my_results.json",  # Default output filename
}
```

### Example Locations

Pre-configured locations for quick testing are available in `config.py`. You can add your own:

```python
EXAMPLE_LOCATIONS = {
    "my_city": {
        "latitude": "12.3456",
        "longitude": "78.9012",
        "description": "My City Name"
    }
}
```

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

1. **"API key not configured"**
   - Copy `config.example.py` to `config.py`
   - Edit `config.py` and add your real API key
   - Or enter API key when prompted

2. **"API key invalid"**
   - Verify your API key is correct
   - Ensure Places API is enabled in Google Cloud Console
   - Check API key restrictions

2. **"No results found"**
   - Try a different keyword
   - Increase the search radius
   - Verify coordinates are correct