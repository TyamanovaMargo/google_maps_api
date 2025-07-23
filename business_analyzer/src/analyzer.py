# src/analyzer.py
import os
import time
from typing import List, Dict, Any
from groq import Groq
from dotenv import load_dotenv
import json

from .models import BusinessData, BusinessAnalysis, QueryResponse
from .utils import split_reviews, parse_business_types, format_price_level, setup_logging

# logger = setup_logging()

# class BusinessAnalysisParser:
#     """Custom parser for business analysis output"""
    
#     def parse(self, text: str) -> Dict[str, Any]:
#         """Parse LLM output into structured format"""
#         try:
#             # Try to parse as JSON first
#             if text.strip().startswith('{'):
#                 return json.loads(text)
            
#             # Fallback to manual parsing
#             lines = text.strip().split('\n')
#             result = {
#                 'summary': '',
#                 'recommendations': [],
#                 'strengths': [],
#                 'weaknesses': [],
#                 'service_quality_score': None,
#                 'staff_behavior_score': None,
#                 'pricing_perception': None,
#                 'user_satisfaction_level': None
#             }
            
#             current_section = None
#             for line in lines:
#                 line = line.strip()
#                 if not line:
#                     continue
                    
#                 if line.lower().startswith('summary:'):
#                     current_section = 'summary'
#                     result['summary'] = line[8:].strip()
#                 elif line.lower().startswith('recommendations:'):
#                     current_section = 'recommendations'
#                 elif line.lower().startswith('strengths:'):
#                     current_section = 'strengths'
#                 elif line.lower().startswith('weaknesses:'):
#                     current_section = 'weaknesses'
#                 elif current_section and line.startswith('-'):
#                     if current_section in ['recommendations', 'strengths', 'weaknesses']:
#                         result[current_section].append(line[1:].strip())
            
#             return result
            
#         except Exception as e:
#             logger.error(f"Failed to parse analysis output: {e}")
#             return {
#                 'summary': text[:200] + '...' if len(text) > 200 else text,
#                 'recommendations': ['Unable to parse detailed recommendations'],
#                 'strengths': [],
#                 'weaknesses': []
#             }
import json
import re
import logging

logger = logging.getLogger(__name__)

class BusinessAnalysisParser:
    """Custom parser for business analysis output"""

    def parse(self, text: str) -> Dict[str, Any]:
        """Parse LLM output into structured format"""
        try:
            # 1️⃣ Вырезаем JSON из markdown-блока ```...```
            match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
            if match:
                text = match.group(1)

            # 2️⃣ Пробуем распарсить как JSON
            if text.strip().startswith('{'):
                return json.loads(text)

            # 3️⃣ Фоллбек: ручной парсинг
            lines = text.strip().split('\n')
            result = {
                'summary': '',
                'recommendations': [],
                'strengths': [],
                'weaknesses': [],
                'service_quality_score': None,
                'staff_behavior_score': None,
                'pricing_perception': None,
                'user_satisfaction_level': None
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
                'user_satisfaction_level': None
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
    """Main analyzer class using Groq API directly"""
    
    def __init__(self, groq_api_key: str = None):
        # Load environment variables first
        load_dotenv()
        self.groq_api_key = groq_api_key or os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Please set it in your .env file or environment variables.\n"
                "Create a .env file with: GROQ_API_KEY=your_actual_api_key"
            )
        self.client = Groq(api_key=self.groq_api_key)  # overwrite всё


        
        self.client = Groq(api_key=self.groq_api_key)
        self.parser = BusinessAnalysisParser()
        self._setup_prompts()
    
    def _setup_prompts(self):
        """Initialize prompt templates"""
        self.analysis_prompt = PromptTemplate(
            input_variables=["name", "address", "rating", "total_ratings", "price_level", 
                           "business_types", "reviews", "location"],
            template="""
            Analyze the following business comprehensively:
            
            Business Name: {name}
            Address: {address}
            Rating: {rating}/5.0 ({total_ratings} total ratings)
            Price Level: {price_level}
            Business Types: {business_types}
            Location: {location}
            
            Customer Reviews:
            {reviews}
            
            Please provide a detailed analysis in the following JSON format:
            {{
                "summary": "A comprehensive 2-3 sentence summary of the business",
                "recommendations": ["specific actionable recommendation 1", "recommendation 2", "recommendation 3"],
                "strengths": ["strength 1", "strength 2", "strength 3"],
                "weaknesses": ["weakness 1", "weakness 2"],
                "service_quality_score": 0.0-10.0,
                "staff_behavior_score": 0.0-10.0,
                "pricing_perception": "expensive/moderate/affordable/unknown",
                "user_satisfaction_level": "high/medium/low"
            }}
            
            Base your analysis on the reviews, ratings, and metadata provided.
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
    
    def analyze_business(self, business: BusinessData) -> BusinessAnalysis:
        """Analyze a single business using Groq"""
        try:
            # Prepare data for analysis
            reviews_list = split_reviews(business.reviews)
            reviews_text = '\n'.join([f"- {review}" for review in reviews_list[:10]])  # Limit to first 10 reviews
            if len(reviews_list) > 10:
                reviews_text += f"\n... and {len(reviews_list) - 10} more reviews"
            
            business_types = ', '.join(parse_business_types(business.types))
            price_level = format_price_level(business.price_level)
            location = f"{business.lat}, {business.lng}"
            
            # Format prompt
            prompt = self.analysis_prompt.format(
                name=business.name,
                address=business.address,
                rating=business.rating,
                total_ratings=int(business.user_ratings_total),
                price_level=price_level,
                business_types=business_types,
                reviews=reviews_text,
                location=location
            )
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            
            print("🤖 MODEL RESPONSE:\n", response.choices[0].message.content)
            # Parse response
            analysis_data = self.parser.parse(response.choices[0].message.content)
            
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
        """Analyze multiple businesses"""
        analyses = []
        total = len(businesses)
        
        logger.info(f"Starting analysis of {total} businesses")
        
        for idx, business in enumerate(businesses):
            logger.info(f"Analyzing business {idx + 1}/{total}: {business.name}")
            analysis = self.analyze_business(business)
            analyses.append(analysis)
            
        time.sleep(1.2)
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
