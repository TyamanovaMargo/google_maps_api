# src/loader.py
import json
from typing import List, Dict, Any
from .models import BusinessData
from .utils import load_json, setup_logging

logger = setup_logging()

class BusinessDataLoader:
    """Handles loading and preprocessing of business data"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.raw_data: List[Dict[str, Any]] = []
        self.businesses: List[BusinessData] = []
    
    def load_data(self) -> None:
        """Load raw data from JSON file"""
        try:
            self.raw_data = load_json(self.filepath)
            logger.info(f"Loaded {len(self.raw_data)} business records from {self.filepath}")
        except FileNotFoundError:
            logger.error(f"Data file not found: {self.filepath}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format: {e}")
            raise
    
    def parse_businesses(self) -> None:
        """Parse raw data into BusinessData objects"""
        parsed_count = 0
        errors = 0
        
        for idx, data in enumerate(self.raw_data):
            try:
                business = BusinessData(**data)
                self.businesses.append(business)
                parsed_count += 1
            except Exception as e:
                logger.warning(f"Failed to parse business at index {idx}: {e}")
                errors += 1
        
        logger.info(f"Successfully parsed {parsed_count} businesses, {errors} errors")
    
    def get_businesses(self) -> List[BusinessData]:
        """Get list of parsed businesses"""
        if not self.businesses:
            self.load_data()
            self.parse_businesses()
        return self.businesses
    
    def filter_by_rating(self, min_rating: float = 0.0, max_rating: float = 5.0) -> List[BusinessData]:
        """Filter businesses by rating range"""
        return [b for b in self.get_businesses() 
                if min_rating <= b.rating <= max_rating]
    
    def filter_by_review_count(self, min_reviews: int = 0) -> List[BusinessData]:
        """Filter businesses by minimum number of reviews"""
        return [b for b in self.get_businesses() 
                if b.user_ratings_total >= min_reviews]
    
    def get_business_by_name(self, name: str) -> BusinessData:
        """Get specific business by name"""
        for business in self.get_businesses():
            if business.name.lower() == name.lower():
                return business
        raise ValueError(f"Business '{name}' not found")