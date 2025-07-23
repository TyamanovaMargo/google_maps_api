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





   # Places Analysis Project

A modular Python project for analyzing and visualizing Google Places API data with review mining and chatbot query.

## Features

- Extracts places information with reviews, ratings, categories, price levels
- Analyzes reviews for keywords and sentiment (optional)
- Analyzes categories and visualizes statistics
- Visualizes distributions of ratings, reviews count, and price levels
- Generates summary reports in CSV, JSON, and text
- Provides LangChain-powered chatbot for querying the data

## Project Structure
```
places_analysis/
├── data/                      # JSON input files
├── notebooks/                 # Jupyter exploration notebooks
├── pipeline/
│   ├── pipeline_runner.py     # Main pipeline steps
│   ├── save_results.py        # Save results to CSV/JSON/report
│   └── run_all.py             # Full pipeline with visualizations & saving
├── reports/                   # Generated reports & visualizations
├── scripts/
│   ├── extract_places.py      # Extracts places and reviews
│   ├── analyze_reviews.py     # Extracts keywords (optional)
│   ├── category_analysis.py   # Analyzes categories
│   ├── visualize_data.py      # Visualizations
│   
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the full pipeline with saving results & visualizations
```bash
python -m pipeline.run_all


```
This will:
- Extract places and reviews from `data/places_results.json`
- Analyze categories
- Visualize:
  - Top categories
  - Ratings distribution
  - Reviews count distribution
  - Price level distribution
- Save CSV, JSON, and summary report to `reports/`

### 3️⃣ Explore data manually in Jupyter
Open:
```
notebooks/exploration.ipynb
```

### 4️⃣ Query your data with LangChain-powered chatbot
```python
from scripts.llm_query_agent import create_llm_agent
agent = create_llm_agent('data/places_llm_data.jsonl')
result = agent.invoke("Show me top-rated restaurants in Shinjuku")
print(result['result'])
```

---

## Recommended Visualizations Functions (from scripts/visualize_data.py)

- `plot_top_categories(categories_series)`
- `plot_ratings_distribution(df)`
- `plot_reviews_count_distribution(df)`
- `plot_price_level_distribution(df)`

---

## Example Command to Save Results
```python
from pipeline.save_results import save_to_csv, save_to_json, save_report

save_to_csv(df, 'reports/places_results.csv')
save_to_json(df, 'reports/places_results.json')
save_report("Top categories:\n" + str(categories.head(10)), 'reports/summary.txt')
```

---

## Requirements
```
pandas==2.2.2
matplotlib==3.8.4
seaborn==0.13.2
nltk==3.8.1
langchain==0.2.0
openai==1.30.1
faiss-cpu==1.8.0
```

---

## ✅ Project ready for:
- Data exploration
- Automated pipeline
- Report generation
- LLM-based question answering on your places data



Here is the `README.md` content in proper Markdown format:

```markdown
# 🧠 places_groq_query

**LLM-powered analyzer for real-world places** (e.g., cafes, restaurants, stores) using structured metadata and customer reviews.  
The project generates AI-based business insights using LangChain and Groq/OpenAI.

---

## 📦 Features

- ✅ Load and parse place metadata from `.json` files  
- 🤖 Generate detailed prompts from full metadata and reviews  
- 🔍 Send them to an LLM (Groq or OpenAI) using a modular client  
- 📈 Receive clear recommendations, quality signals, and insights  
- 💾 Save all results to a structured JSON file

---

## 🗂 Project Structure

```

places\_groq\_query/
├── main.py               # Launches the full analysis pipeline
├── analyzer.py           # Builds prompts and handles LLM analysis
├── file\_loader.py        # Loads place metadata from JSON files
├── groq\_client.py        # Builds prompts and sends requests to LLM
├── logger.py             # Structured logging output
├── config.py             # Placeholder for shared settings
├── **init**.py
data/
├── my\_places.json        # Your input file with places
reports/
├── places\_analysis.json  # Final output with results

````

---

## 🧪 Input Format

Your JSON file in `data/` should contain a list of dictionaries with the following fields:

```json
[
  {
    "name": "Cafe Aroma",
    "rating": 4.6,
    "user_ratings_total": 120,
    "price_level": 2,
    "types": ["cafe", "restaurant"],
    "lat": 32.0853,
    "lng": 34.7818,
    "reviews": [
      "Great coffee and cozy atmosphere.",
      "Staff were kind but service was slow."
    ]
  }
]
````

---

## 🚀 How to Run

1. **Install dependencies** (in a virtual environment recommended):

```bash
pip install -r requirements.txt
```

2. **Set your API key** for OpenAI or Groq:

```bash
export OPENAI_API_KEY=your-key-here
```

3. **Run the analysis**:

```bash
python3 -m places_groq_query.main
```

Results will be saved to:

```
reports/places_analysis.json
```

---

## 📤 Output Example

```json
[
  {
    "name": "Cafe Aroma",
    "analysis": "This place is successful due to its consistent service quality, positive customer reviews, and comfortable ambiance. However, it could improve by addressing wait times during peak hours."
  }
]
```

---

## 🧠 Prompts & LLM Behavior

Each place is sent to the LLM with:

* Full metadata (as JSON)
* Up to 5 real user reviews
* A reusable instruction:
  *"Analyze the place. Identify strengths and weaknesses. Provide actionable insights."*

---

## 🛠 To Customize

* 🔧 Modify prompt behavior in `groq_client.py → build_prompt()`
* 🧠 Switch LLM providers via `send_prompt()`
* 📁 Add CSV/JSON writers or visualizations in `result_writer.py` (optional)

---

## 📃 License

MIT — free to use and modify.


# Project Structure
business_analyzer/
├── main.py
├── src/
│   ├── __init__.py
│   ├── loader.py
│   ├── analyzer.py
│   ├── models.py
│   └── utils.py
├── reports/
│   └── analysis_output.json
├── data/
│   └── business_data.json
├── .env.example
├── requirements.txt
└── README.md



# README.md
# Business Places Analyzer

A comprehensive Python project that analyzes business places using metadata and customer reviews through LangChain and Groq integration.

## Features

- **Data Loading**: Parse JSON files containing business metadata and reviews
- **Semantic Analysis**: Analyze strengths, weaknesses, service quality, staff behavior, pricing, and user satisfaction using Groq API
- **Query System**: Ask general questions about businesses and get insights
- **Structured Output**: Generate structured reports with summaries and recommendations

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env file and add your Groq API key
   ```
   Or set directly:
   ```bash
   export GROQ_API_KEY="your_groq_api_key_here"
   ```

## Usage

1. Place your business data JSON file in the `data/` directory
2. Run the analyzer:
   ```bash
   python main.py
   ```
3. Check the results in `reports/analysis_output.json`

## Project Structure

- `main.py`: Entry point and orchestration
- `src/loader.py`: Data loading and preprocessing
- `src/analyzer.py`: Core analysis logic using LangChain and Groq
- `src/models.py`: Data models and schemas
- `src/utils.py`: Utility functions
- `reports/`: Output directory for analysis results

## Data Format

Input JSON should contain business entries with fields:
- name, address, rating, user_ratings_total
- price_level, types, lat, lng
- reviews (pipe-separated string)

## Output Format

Analysis results are saved as structured JSON with summaries and recommendations for each business.

## Environment Variables

Create a `.env` file in the root directory with:
```
GROQ_API_KEY=your_groq_api_key_here
```


