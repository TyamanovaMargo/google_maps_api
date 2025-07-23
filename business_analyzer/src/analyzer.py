# src/analyzer.py
import os
import time
from typing import List, Dict, Any, Tuple
from groq import Groq
from dotenv import load_dotenv
import json
import re
import logging

from .models import BusinessData, BusinessAnalysis, QueryResponse
from .utils import split_reviews, parse_business_types, format_price_level, setup_logging

logger = logging.getLogger(__name__)

class SentimentAnalysis:
    """Class to hold sentiment analysis results"""
    def __init__(self, sentiment: str, confidence: float, emotions: List[str] = None):
        self.sentiment = sentiment  # 'positive', 'negative', 'neutral'
        self.confidence = confidence  # 0.0 to 1.0
        self.emotions = emotions or []  # ['happy', 'frustrated', 'satisfied', etc.]

class ReviewWithSentiment:
    """Class to hold review text with its sentiment analysis"""
    def __init__(self, text: str, sentiment_analysis: SentimentAnalysis):
        self.text = text
        self.sentiment = sentiment_analysis

class BusinessAnalysisParser:
    """Custom parser for business analysis output"""

    def parse(self, text: str) -> Dict[str, Any]:
        """Parse LLM output into structured format"""
        try:
            # 1️⃣ Extract JSON from markdown block ```...```
            match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
            if match:
                text = match.group(1)

            # 2️⃣ Try to parse as JSON
            if text.strip().startswith('{'):
                return json.loads(text)

            # 3️⃣ Fallback: manual parsing
            lines = text.strip().split('\n')
            result = {
                'summary': '',
                'recommendations': [],
                'strengths': [],
                'weaknesses': [],
                'service_quality_score': None,
                'staff_behavior_score': None,
                'pricing_perception': None,
                'user_satisfaction_level': None,
                'sentiment_summary': None,
                'review_sentiments': []
            }

            current_section = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                if line.lower().startswith('summary:'):
                    current_section = 'summary'
                    result['summary'] = line[8:].strip()
                elif line.lower().startswith('recommendations:'):
                    current_section = 'recommendations'
                elif line.lower().startswith('strengths:'):
                    current_section = 'strengths'
                elif line.lower().startswith('weaknesses:'):
                    current_section = 'weaknesses'
                elif current_section and line.startswith('-'):
                    result[current_section].append(line[1:].strip())

            return result

        except Exception as e:
            logger.error(f"Failed to parse analysis output: {e}")
            return {
                'summary': text[:200] + '...' if len(text) > 200 else text,
                'recommendations': ['Unable to parse detailed recommendations'],
                'strengths': [],
                'weaknesses': [],
                'service_quality_score': None,
                'staff_behavior_score': None,
                'pricing_perception': None,
                'user_satisfaction_level': None,
                'sentiment_summary': None,
                'review_sentiments': []
            }

class PromptTemplate:
    """Simple prompt template class"""
    
    def __init__(self, input_variables: List[str], template: str):
        self.input_variables = input_variables
        self.template = template
    
    def format(self, **kwargs) -> str:
        """Format template with provided variables"""
        return self.template.format(**kwargs)

class BusinessAnalyzer:
    """Main analyzer class using Groq API directly with sentiment analysis"""
    
    def __init__(self, groq_api_key: str = None):
        # Load environment variables first
        load_dotenv()
        self.groq_api_key = groq_api_key or os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Please set it in your .env file or environment variables.\n"
                "Create a .env file with: GROQ_API_KEY=your_actual_api_key"
            )
        
        self.client = Groq(api_key=self.groq_api_key)
        self.parser = BusinessAnalysisParser()
        self._setup_prompts()
    
    def _setup_prompts(self):
        """Initialize prompt templates"""
        self.sentiment_prompt = PromptTemplate(
            input_variables=["reviews"],
            template="""
            Analyze the sentiment of the following customer reviews. For each review, determine:
            1. Overall sentiment (positive, negative, neutral)
            2. Confidence level (0.0 to 1.0)
            3. Specific emotions detected (happy, frustrated, satisfied, angry, disappointed, excited, etc.)
            
            Reviews:
            {reviews}
            
            Please provide the analysis in the following JSON format:
            {{
                "reviews": [
                    {{
                        "text": "original review text",
                        "sentiment": "positive/negative/neutral",
                        "confidence": 0.85,
                        "emotions": ["happy", "satisfied"]
                    }}
                ],
                "overall_sentiment_distribution": {{
                    "positive": 0.6,
                    "negative": 0.2,
                    "neutral": 0.2
                }},
                "dominant_emotions": ["satisfied", "happy", "frustrated"],
                "sentiment_summary": "Brief summary of overall customer sentiment"
            }}
            """
        )
        
        self.analysis_prompt = PromptTemplate(
            input_variables=["name", "address", "rating", "total_ratings", "price_level", 
                           "business_types", "reviews", "location", "sentiment_data"],
            template="""
            Analyze the following business comprehensively, including sentiment analysis data:
            
            Business Name: {name}
            Address: {address}
            Rating: {rating}/5.0 ({total_ratings} total ratings)
            Price Level: {price_level}
            Business Types: {business_types}
            Location: {location}
            
            Customer Reviews:
            {reviews}
            
            Sentiment Analysis Data:
            {sentiment_data}
            
            Please provide a detailed analysis in the following JSON format:
            {{
                "summary": "A comprehensive 2-3 sentence summary of the business including sentiment insights",
                "recommendations": ["specific actionable recommendation 1", "recommendation 2", "recommendation 3"],
                "strengths": ["strength 1", "strength 2", "strength 3"],
                "weaknesses": ["weakness 1", "weakness 2"],
                "service_quality_score": 0.0-10.0,
                "staff_behavior_score": 0.0-10.0,
                "pricing_perception": "expensive/moderate/affordable/unknown",
                "user_satisfaction_level": "high/medium/low",
                "sentiment_summary": {{
                    "overall_sentiment": "positive/negative/neutral",
                    "positive_percentage": 0.0-1.0,
                    "negative_percentage": 0.0-1.0,
                    "neutral_percentage": 0.0-1.0,
                    "dominant_emotions": ["emotion1", "emotion2"],
                    "sentiment_trends": "Brief description of sentiment patterns"
                }}
            }}
            
            Base your analysis on the reviews, ratings, metadata, and sentiment analysis provided.
            """
        )
        
        self.query_prompt = PromptTemplate(
            input_variables=["question", "businesses_data"],
            template="""
            Based on the following business data, answer this question: {question}
            
            Business Data:
            {businesses_data}
            
            Provide a comprehensive answer that references specific businesses when relevant.
            Include business names in your response when they support your answer.
            """
        )
    
    def analyze_review_sentiments(self, reviews: List[str]) -> Dict[str, Any]:
        """Analyze sentiment for a list of reviews"""
        try:
            # Limit reviews for API efficiency
            reviews_to_analyze = reviews[:15]  # Analyze first 15 reviews
            reviews_text = '\n'.join([f"{i+1}. {review}" for i, review in enumerate(reviews_to_analyze)])
            
            # Format prompt
            prompt = self.sentiment_prompt.format(reviews=reviews_text)
            
            # Call Groq API for sentiment analysis
            response = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # Lower temperature for more consistent sentiment analysis
                max_tokens=1500
            )
            
            # Parse sentiment response
            sentiment_text = response.choices[0].message.content
            
            # Extract JSON from response
            match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", sentiment_text, re.DOTALL)
            if match:
                sentiment_data = json.loads(match.group(1))
            elif sentiment_text.strip().startswith('{'):
                sentiment_data = json.loads(sentiment_text)
            else:
                # Fallback sentiment analysis
                logger.warning("Could not parse sentiment JSON, using fallback")
                return self._fallback_sentiment_analysis(reviews_to_analyze)
            
            return sentiment_data
            
        except Exception as e:
            logger.error(f"Failed to analyze sentiments: {e}")
            return self._fallback_sentiment_analysis(reviews)
    
    def _fallback_sentiment_analysis(self, reviews: List[str]) -> Dict[str, Any]:
        """Simple fallback sentiment analysis"""
        positive_keywords = ['good', 'great', 'excellent', 'amazing', 'love', 'perfect', 'wonderful']
        negative_keywords = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'disappointing']
        
        review_sentiments = []
        positive_count = 0
        negative_count = 0
        
        for review in reviews[:10]:  # Analyze first 10 reviews
            review_lower = review.lower()
            positive_score = sum(1 for word in positive_keywords if word in review_lower)
            negative_score = sum(1 for word in negative_keywords if word in review_lower)
            
            if positive_score > negative_score:
                sentiment = "positive"
                positive_count += 1
            elif negative_score > positive_score:
                sentiment = "negative"
                negative_count += 1
            else:
                sentiment = "neutral"
            
            review_sentiments.append({
                "text": review[:100] + "..." if len(review) > 100 else review,
                "sentiment": sentiment,
                "confidence": 0.6,  # Default confidence for fallback
                "emotions": []
            })
        
        total_reviews = len(review_sentiments)
        neutral_count = total_reviews - positive_count - negative_count
        
        return {
            "reviews": review_sentiments,
            "overall_sentiment_distribution": {
                "positive": positive_count / total_reviews if total_reviews > 0 else 0,
                "negative": negative_count / total_reviews if total_reviews > 0 else 0,
                "neutral": neutral_count / total_reviews if total_reviews > 0 else 0
            },
            "dominant_emotions": ["satisfied"] if positive_count > negative_count else ["frustrated"],
            "sentiment_summary": f"Basic sentiment analysis: {positive_count} positive, {negative_count} negative, {neutral_count} neutral reviews"
        }
    
    def analyze_business(self, business: BusinessData) -> BusinessAnalysis:
        """Analyze a single business using Groq with sentiment analysis"""
        try:
            # Prepare reviews data
            reviews_list = split_reviews(business.reviews)
            
            # Step 1: Analyze sentiment of reviews
            logger.info(f"Analyzing sentiment for {business.name}")
            sentiment_data = self.analyze_review_sentiments(reviews_list)
            
            # Step 2: Prepare data for business analysis
            reviews_text = '\n'.join([f"- {review}" for review in reviews_list[:10]])
            if len(reviews_list) > 10:
                reviews_text += f"\n... and {len(reviews_list) - 10} more reviews"
            
            business_types = ', '.join(parse_business_types(business.types))
            price_level = format_price_level(business.price_level)
            location = f"{business.lat}, {business.lng}"
            
            # Format sentiment data for prompt
            sentiment_summary = json.dumps(sentiment_data, indent=2)
            
            # Format prompt
            prompt = self.analysis_prompt.format(
                name=business.name,
                address=business.address,
                rating=business.rating,
                total_ratings=int(business.user_ratings_total),
                price_level=price_level,
                business_types=business_types,
                reviews=reviews_text,
                location=location,
                sentiment_data=sentiment_summary
            )
            
            # Call Groq API for business analysis
            response = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1200
            )
            
            print("🤖 MODEL RESPONSE:\n", response.choices[0].message.content)
            
            # Parse response
            analysis_data = self.parser.parse(response.choices[0].message.content)
            
            # Add sentiment data to analysis
            analysis_data['review_sentiments'] = sentiment_data.get('reviews', [])
            if 'sentiment_summary' not in analysis_data or not analysis_data['sentiment_summary']:
                analysis_data['sentiment_summary'] = sentiment_data
            
            # Create BusinessAnalysis object
            return BusinessAnalysis(
                name=business.name,
                **analysis_data
            )
            
        except Exception as e:
            logger.error(f"Failed to analyze business '{business.name}': {e}")
            return BusinessAnalysis(
                name=business.name,
                summary=f"Analysis failed for {business.name}. Error: {str(e)}",
                recommendations=["Unable to generate recommendations due to analysis error"]
            )
    
    def analyze_multiple_businesses(self, businesses: List[BusinessData]) -> List[BusinessAnalysis]:
        """Analyze multiple businesses with sentiment analysis"""
        analyses = []
        total = len(businesses)
        
        logger.info(f"Starting analysis of {total} businesses with sentiment analysis")
        
        for idx, business in enumerate(businesses):
            logger.info(f"Analyzing business {idx + 1}/{total}: {business.name}")
            analysis = self.analyze_business(business)
            analyses.append(analysis)
            
            # Rate limiting - pause between requests
            time.sleep(1.5)
        
        logger.info(f"Completed analysis of {len(analyses)} businesses")
        return analyses
    
    def query_businesses(self, question: str, businesses: List[BusinessData]) -> QueryResponse:
        """Answer questions about businesses"""
        try:
            # Prepare business data summary for query
            business_summaries = []
            for business in businesses:
                summary = (
                    f"Name: {business.name}, "
                    f"Rating: {business.rating}/5.0 ({int(business.user_ratings_total)} reviews), "
                    f"Types: {business.types}, "
                    f"Price: {format_price_level(business.price_level)}"
                )
                business_summaries.append(summary)
            
            businesses_data = '\n'.join(business_summaries)
            
            # Format prompt
            prompt = self.query_prompt.format(
                question=question,
                businesses_data=businesses_data
            )
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=800
            )
            
            answer = response.choices[0].message.content
            
            # Extract mentioned business names
            supporting_businesses = []
            for business in businesses:
                if business.name.lower() in answer.lower():
                    supporting_businesses.append(business.name)
            
            return QueryResponse(
                question=question,
                answer=answer,
                supporting_businesses=supporting_businesses
            )
            
        except Exception as e:
            logger.error(f"Failed to process query '{question}': {e}")
            return QueryResponse(
                question=question,
                answer=f"Sorry, I couldn't process your question due to an error: {str(e)}"
            )
    
    def get_sentiment_report(self, analyses: List[BusinessAnalysis]) -> Dict[str, Any]:
        """Generate a comprehensive sentiment report for all analyzed businesses"""
        try:
            total_businesses = len(analyses)
            sentiment_scores = []
            all_emotions = []
            
            for analysis in analyses:
                if hasattr(analysis, 'sentiment_summary') and analysis.sentiment_summary:
                    if isinstance(analysis.sentiment_summary, dict):
                        sentiment_data = analysis.sentiment_summary
                        if 'overall_sentiment_distribution' in sentiment_data:
                            sentiment_scores.append(sentiment_data['overall_sentiment_distribution'])
                        if 'dominant_emotions' in sentiment_data:
                            all_emotions.extend(sentiment_data['dominant_emotions'])
            
            # Calculate overall sentiment distribution
            if sentiment_scores:
                avg_positive = sum(s.get('positive', 0) for s in sentiment_scores) / len(sentiment_scores)
                avg_negative = sum(s.get('negative', 0) for s in sentiment_scores) / len(sentiment_scores)
                avg_neutral = sum(s.get('neutral', 0) for s in sentiment_scores) / len(sentiment_scores)
            else:
                avg_positive = avg_negative = avg_neutral = 0
            
            # Count emotion frequencies
            emotion_counts = {}
            for emotion in all_emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            # Sort emotions by frequency
            top_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return {
                "total_businesses_analyzed": total_businesses,
                "overall_sentiment_distribution": {
                    "positive": round(avg_positive, 3),
                    "negative": round(avg_negative, 3),
                    "neutral": round(avg_neutral, 3)
                },
                "top_emotions": [{"emotion": emotion, "frequency": count} for emotion, count in top_emotions],
                "businesses_with_positive_sentiment": len([a for a in analyses if self._get_business_sentiment(a) == "positive"]),
                "businesses_with_negative_sentiment": len([a for a in analyses if self._get_business_sentiment(a) == "negative"]),
                "sentiment_analysis_summary": f"Analyzed {total_businesses} businesses with average sentiment distribution: {avg_positive:.1%} positive, {avg_negative:.1%} negative, {avg_neutral:.1%} neutral"
            }
            
        except Exception as e:
            logger.error(f"Failed to generate sentiment report: {e}")
            return {"error": f"Could not generate sentiment report: {str(e)}"}
    
    def _get_business_sentiment(self, analysis: BusinessAnalysis) -> str:
        """Extract overall sentiment for a business analysis"""
        try:
            if hasattr(analysis, 'sentiment_summary') and analysis.sentiment_summary:
                if isinstance(analysis.sentiment_summary, dict):
                    if 'overall_sentiment' in analysis.sentiment_summary:
                        return analysis.sentiment_summary['overall_sentiment']
                    elif 'overall_sentiment_distribution' in analysis.sentiment_summary:
                        dist = analysis.sentiment_summary['overall_sentiment_distribution']
                        if dist.get('positive', 0) > max(dist.get('negative', 0), dist.get('neutral', 0)):
                            return "positive"
                        elif dist.get('negative', 0) > dist.get('neutral', 0):
                            return "negative"
                        else:
                            return "neutral"
            return "neutral"
        except:
            return "neutral"


