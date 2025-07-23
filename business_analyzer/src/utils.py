# src/utils.py
import json
import os
from typing import List, Dict, Any
import logging
from typing import Optional

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('business_analyzer.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def ensure_directories():
    """Ensure required directories exist"""
    directories = ['data', 'reports', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def save_json(data: Any, filepath: str) -> None:
    """Save data to JSON file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(filepath: str) -> Any:
    """Load data from JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_price_level(price_level: Optional[int]) -> str:
    """Convert price level to human readable format"""
    if price_level is None:
        return "Unknown"
    mapping = {
        0: "Free",
        1: "Inexpensive", 
        2: "Moderate",
        3: "Expensive",
        4: "Very Expensive"
    }
    return mapping.get(price_level, "Unknown")

def parse_business_types(types: str) -> List[str]:
    """Parse comma-separated business types"""
    return [t.strip() for t in types.split(',') if t.strip()]

def split_reviews(reviews: str) -> List[str]:
    """Split pipe-separated reviews into list"""
    if not reviews:
        return []
    return [review.strip() for review in reviews.split('|||') if review.strip()]