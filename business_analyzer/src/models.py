# src/models.py
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class BusinessData(BaseModel):
    """Model for raw business data from JSON"""
    name: str
    address: str
    rating: float
    user_ratings_total: float
    price_level: Optional[int] = None
    types: str
    lat: float
    lng: float
    reviews: str

class BusinessAnalysis(BaseModel):
    """Model for business analysis results"""
    name: str
    summary: str
    recommendations: List[str]
    
    # Additional analysis fields
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    service_quality_score: Optional[float] = None
    staff_behavior_score: Optional[float] = None
    pricing_perception: Optional[str] = None
    user_satisfaction_level: Optional[str] = None

class QueryResponse(BaseModel):
    """Model for query responses"""
    question: str
    answer: str
    supporting_businesses: List[str] = Field(default_factory=list)