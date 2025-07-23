# src/models.py
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass

@dataclass
class BusinessData:
    """Data class for business information from Google Places API"""
    name: str
    address: str
    rating: float
    user_ratings_total: int
    price_level: Optional[int]
    types: List[str]
    reviews: str  # Combined reviews text
    lat: float
    lng: float
    place_id: str
    
    def __post_init__(self):
        """Validate data after initialization"""
        if not isinstance(self.rating, (int, float)):
            self.rating = 0.0
        if not isinstance(self.user_ratings_total, int):
            self.user_ratings_total = 0
        if self.price_level is not None and not isinstance(self.price_level, int):
            self.price_level = None

@dataclass
class SentimentData:
    """Data class for sentiment analysis results"""
    sentiment: str  # 'positive', 'negative', 'neutral'
    confidence: float  # 0.0 to 1.0
    emotions: List[str]  # List of detected emotions
    
    def __post_init__(self):
        """Validate sentiment data"""
        if self.sentiment not in ['positive', 'negative', 'neutral']:
            self.sentiment = 'neutral'
        if not 0 <= self.confidence <= 1:
            self.confidence = 0.5
        if not isinstance(self.emotions, list):
            self.emotions = []

@dataclass
class ReviewSentiment:
    """Data class for individual review with sentiment"""
    text: str
    sentiment_data: SentimentData
    
    @property
    def sentiment(self) -> str:
        return self.sentiment_data.sentiment
    
    @property
    def confidence(self) -> float:
        return self.sentiment_data.confidence
    
    @property
    def emotions(self) -> List[str]:
        return self.sentiment_data.emotions

@dataclass
class BusinessAnalysis:
    """Data class for business analysis results including sentiment"""
    name: str
    summary: str = ""
    recommendations: List[str] = None
    strengths: List[str] = None
    weaknesses: List[str] = None
    service_quality_score: Optional[float] = None
    staff_behavior_score: Optional[float] = None
    pricing_perception: Optional[str] = None
    user_satisfaction_level: Optional[str] = None
    
    # Sentiment analysis fields
    sentiment_summary: Optional[Union[Dict[str, Any], str]] = None
    review_sentiments: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize default values for list fields"""
        if self.recommendations is None:
            self.recommendations = []
        if self.strengths is None:
            self.strengths = []
        if self.weaknesses is None:
            self.weaknesses = []
        if self.review_sentiments is None:
            self.review_sentiments = []
    
    @property
    def overall_sentiment(self) -> str:
        """Get overall sentiment for the business"""
        if isinstance(self.sentiment_summary, dict):
            if 'overall_sentiment' in self.sentiment_summary:
                return self.sentiment_summary['overall_sentiment']
            elif 'overall_sentiment_distribution' in self.sentiment_summary:
                dist = self.sentiment_summary['overall_sentiment_distribution']
                positive = dist.get('positive', 0)
                negative = dist.get('negative', 0)
                neutral = dist.get('neutral', 0)
                
                if positive > max(negative, neutral):
                    return 'positive'
                elif negative > neutral:
                    return 'negative'
                else:
                    return 'neutral'
        return 'neutral'
    
    @property
    def sentiment_distribution(self) -> Dict[str, float]:
        """Get sentiment distribution percentages"""
        if isinstance(self.sentiment_summary, dict) and 'overall_sentiment_distribution' in self.sentiment_summary:
            return self.sentiment_summary['overall_sentiment_distribution']
        return {'positive': 0.0, 'negative': 0.0, 'neutral': 1.0}
    
    @property
    def dominant_emotions(self) -> List[str]:
        """Get dominant emotions from sentiment analysis"""
        if isinstance(self.sentiment_summary, dict) and 'dominant_emotions' in self.sentiment_summary:
            return self.sentiment_summary['dominant_emotions']
        return []
    
    def get_positive_reviews(self) -> List[Dict[str, Any]]:
        """Get all positive reviews"""
        return [review for review in self.review_sentiments if review.get('sentiment') == 'positive']
    
    def get_negative_reviews(self) -> List[Dict[str, Any]]:
        """Get all negative reviews"""
        return [review for review in self.review_sentiments if review.get('sentiment') == 'negative']
    
    def get_neutral_reviews(self) -> List[Dict[str, Any]]:
        """Get all neutral reviews"""
        return [review for review in self.review_sentiments if review.get('sentiment') == 'neutral']
    
    def get_sentiment_score(self) -> float:
        """Calculate a sentiment score from -1 (very negative) to 1 (very positive)"""
        dist = self.sentiment_distribution
        return dist.get('positive', 0) - dist.get('negative', 0)
    
    def has_sentiment_data(self) -> bool:
        """Check if sentiment analysis data is available"""
        return bool(self.sentiment_summary and self.review_sentiments)

@dataclass
class QueryResponse:
    """Data class for query responses"""
    question: str
    answer: str
    supporting_businesses: List[str] = None
    confidence_score: Optional[float] = None
    
    def __post_init__(self):
        """Initialize default values"""
        if self.supporting_businesses is None:
            self.supporting_businesses = []

@dataclass
class SentimentReport:
    """Data class for comprehensive sentiment analysis report"""
    total_businesses: int
    overall_sentiment_distribution: Dict[str, float]
    top_emotions: List[Dict[str, Union[str, int]]]
    businesses_by_sentiment: Dict[str, List[str]]
    sentiment_trends: Optional[str] = None
    
    @property
    def positive_businesses_count(self) -> int:
        """Get count of businesses with positive sentiment"""
        return len(self.businesses_by_sentiment.get('positive', []))
    
    @property
    def negative_businesses_count(self) -> int:
        """Get count of businesses with negative sentiment"""
        return len(self.businesses_by_sentiment.get('negative', []))
    
    @property
    def neutral_businesses_count(self) -> int:
        """Get count of businesses with neutral sentiment"""
        return len(self.businesses_by_sentiment.get('neutral', []))
    
    def get_most_common_emotion(self) -> Optional[str]:
        """Get the most frequently detected emotion"""
        if self.top_emotions:
            return self.top_emotions[0]['emotion']
        return None
    
    def get_sentiment_summary(self) -> str:
        """Get a human-readable summary of sentiment analysis"""
        positive_pct = self.overall_sentiment_distribution.get('positive', 0) * 100
        negative_pct = self.overall_sentiment_distribution.get('negative', 0) * 100
        neutral_pct = self.overall_sentiment_distribution.get('neutral', 0) * 100
        
        return (f"Analyzed {self.total_businesses} businesses: "
                f"{positive_pct:.1f}% positive, {negative_pct:.1f}% negative, "
                f"{neutral_pct:.1f}% neutral sentiment")

# Helper functions for working with models

def create_business_analysis_with_sentiment(
    name: str,
    analysis_data: Dict[str, Any],
    sentiment_data: Dict[str, Any]
) -> BusinessAnalysis:
    """Helper function to create BusinessAnalysis with sentiment data"""
    
    return BusinessAnalysis(
        name=name,
        summary=analysis_data.get('summary', ''),
        recommendations=analysis_data.get('recommendations', []),
        strengths=analysis_data.get('strengths', []),
        weaknesses=analysis_data.get('weaknesses', []),
        service_quality_score=analysis_data.get('service_quality_score'),
        staff_behavior_score=analysis_data.get('staff_behavior_score'),
        pricing_perception=analysis_data.get('pricing_perception'),
        user_satisfaction_level=analysis_data.get('user_satisfaction_level'),
        sentiment_summary=sentiment_data,
        review_sentiments=sentiment_data.get('reviews', [])
    )

def aggregate_sentiment_data(analyses: List[BusinessAnalysis]) -> SentimentReport:
    """Aggregate sentiment data from multiple business analyses"""
    if not analyses:
        return SentimentReport(
            total_businesses=0,
            overall_sentiment_distribution={'positive': 0, 'negative': 0, 'neutral': 0},
            top_emotions=[],
            businesses_by_sentiment={'positive': [], 'negative': [], 'neutral': []}
        )
    
    # Collect sentiment data
    total_positive = total_negative = total_neutral = 0
    all_emotions = []
    businesses_by_sentiment = {'positive': [], 'negative': [], 'neutral': []}
    
    for analysis in analyses:
        sentiment = analysis.overall_sentiment
        businesses_by_sentiment[sentiment].append(analysis.name)
        
        # Count sentiment distribution
        dist = analysis.sentiment_distribution
        total_positive += dist.get('positive', 0)
        total_negative += dist.get('negative', 0)
        total_neutral += dist.get('neutral', 0)
        
        # Collect emotions
        all_emotions.extend(analysis.dominant_emotions)
    
    # Calculate averages
    total_businesses = len(analyses)
    avg_positive = total_positive / total_businesses if total_businesses > 0 else 0
    avg_negative = total_negative / total_businesses if total_businesses > 0 else 