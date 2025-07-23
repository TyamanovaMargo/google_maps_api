# example_usage_with_sentiment.py
"""
Example usage of the enhanced BusinessAnalyzer with sentiment analysis
"""

import os
from src.analyzer import BusinessAnalyzer
from src.models import BusinessData, aggregate_sentiment_data, filter_businesses_by_sentiment
from src.utils import setup_logging

# Setup logging
logger = setup_logging()

def main():
    # Initialize analyzer
    analyzer = BusinessAnalyzer()
    
    # Example business data (you would typically load this from Google Places API)
    sample_businesses = [
        BusinessData(
            name="Amazing Coffee Shop",
            address="123 Main St, City",
            rating=4.5,
            user_ratings_total=150,
            price_level=2,
            types=["cafe", "restaurant"],
            reviews="Great coffee and friendly staff! The atmosphere is cozy and perfect for working. Love coming here every morning. Best cappuccino in town! However, sometimes it gets too crowded. The wifi is fast and reliable.",
            lat=40.7128,
            lng=-74.0060,
            place_id="example_place_id_1"
        ),
        BusinessData(
            name="Terrible Pizza Place",
            address="456 Oak Ave, City",
            rating=2.1,
            user_ratings_total=89,
            price_level=1,
            types=["restaurant", "meal_delivery"],
            reviews="Worst pizza I've ever had. Cold, soggy, and overpriced. Staff was rude and unhelpful. Never ordering from here again. Disappointed with the service. The place looks dirty and unprofessional.",
            lat=40.7589,
            lng=-73.9851,
            place_id="example_place_id_2"
        ),
        BusinessData(
            name="Decent Burger Joint",
            address="789 Pine St, City",
            rating=3.8,
            user_ratings_total=245,
            price_level=2,
            types=["restaurant", "food"],
            reviews="The burgers are okay, nothing special. Service is average. Good fries though. It's a decent place for a quick meal. Sometimes the wait is long but the food is consistent. Fair prices for the quality.",
            lat=40.7505,
            lng=-73.9934,
            place_id="example_place_id_3"
        )
    ]
    
    print("🔍 Starting Business Analysis with Sentiment Analysis...")
    print("=" * 60)
    
    # Analyze all businesses
    analyses = analyzer.analyze_multiple_businesses(sample_businesses)
    
    print(f"\n📊 Analysis completed for {len(analyses)} businesses!")
    print("=" * 60)
    
    # Display detailed results for each business
    for analysis in analyses:
        print(f"\n🏢 Business: {analysis.name}")
        print(f"📝 Summary: {analysis.summary}")
        print(f"😊 Overall Sentiment: {analysis.overall_sentiment}")
        
        # Display sentiment distribution
        dist = analysis.sentiment_distribution
        print(f"📊 Sentiment Distribution:")
        print(f"   ✅ Positive: {dist['positive']:.1%}")
        print(f"   ❌ Negative: {dist['negative']:.1%}")
        print(f"   ⚪ Neutral: {dist['neutral']:.1%}")
        
        # Display dominant emotions
        if analysis.dominant_emotions:
            print(f"🎭 Dominant Emotions: {', '.join(analysis.dominant_emotions)}")
        
        # Display sample review sentiments
        if analysis.review_sentiments:
            print(f"💬 Sample Review Sentiments:")
            for i, review in enumerate(analysis.review_sentiments[:3]):  # Show first 3
                emoji = "😊" if review['sentiment'] == 'positive' else "😞" if review['sentiment'] == 'negative' else "😐"
                print(f"   {emoji} \"{review['text'][:60]}...\" ({review['sentiment']}, {review['confidence']:.2f})")
        
        # Display strengths and weaknesses
        if analysis.strengths:
            print(f"💪 Strengths: {', '.join(analysis.strengths[:3])}")
        if analysis.weaknesses:
            print(f"⚠️  Weaknesses: {', '.join(analysis.weaknesses[:3])}")
        
        # Display recommendations
        if analysis.recommendations:
            print(f"💡 Top Recommendations:")
            for i, rec in enumerate(analysis.recommendations[:2], 1):
                print(f"   {i}. {rec}")
        
        print("-" * 50)
    
    # Generate overall sentiment report
    print(f"\n📈 OVERALL SENTIMENT REPORT")
    print("=" * 60)
    
    sentiment_report = aggregate_sentiment_data(analyses)
    print(f"🏢 Total Businesses Analyzed: {sentiment_report.total_businesses}")
    print(f"📊 Overall Sentiment Distribution:")
    print(f"   ✅ Positive: {sentiment_report.overall_sentiment_distribution['positive']:.1%}")
    print(f"   ❌ Negative: {sentiment_report.overall_sentiment_distribution['negative']:.1%}")
    print(f"   ⚪ Neutral: {sentiment_report.overall_sentiment_distribution['neutral']:.1%}")
    
    print(f"\n🎭 Top Emotions Detected:")
    for emotion_data in sentiment_report.top_emotions[:5]:
        print(f"   • {emotion_data['emotion']}: {emotion_data['frequency']} mentions")
    
    print(f"\n🏆 Business Categories by Sentiment:")
    print(f"   😊 Positive Businesses: {', '.join(sentiment_report.businesses_by_sentiment['positive'])}")
    print(f"   😞 Negative Businesses: {', '.join(sentiment_report.businesses_by_sentiment['negative'])}")
    print(f"   😐 Neutral Businesses: {', '.join(sentiment_report.businesses_by_sentiment['neutral'])}")
    
    # Filter businesses by sentiment
    print(f"\n🔍 FILTERING EXAMPLES")
    print("=" * 60)
    
    positive_businesses = filter_businesses_by_sentiment(analyses, 'positive')
    print(f"✅ Positive Businesses ({len(positive_businesses)}):")
    for business in positive_businesses:
        score = business.get_sentiment_score()
        print(f"   • {business.name} (Sentiment Score: {score:.2f})")
    
    negative_businesses = filter_businesses_by_sentiment(analyses, 'negative')
    print(f"\n❌ Negative Businesses ({len(negative_businesses)}):")
    for business in negative_businesses:
        score = business.get_sentiment_score()
        print(f"   • {business.name} (Sentiment Score: {score:.2f})")
    
    # Example query with sentiment context
    print(f"\n❓ EXAMPLE QUERY WITH SENTIMENT CONTEXT")
    print("=" * 60)
    
    query = "Which businesses have the most positive customer sentiment?"
    response = analyzer.query_businesses(query, sample_businesses)
    print(f"Question: {response.question}")
    print(f"Answer: {response.answer}")
    if response.supporting_businesses:
        print(f"Supporting Businesses: {', '.join(response.supporting_businesses)}")
    
    # Advanced sentiment analysis features
    print(f"\n🔬 ADVANCED SENTIMENT FEATURES")
    print("=" * 60)
    
    for analysis in analyses:
        if analysis.has_sentiment_data():
            positive_reviews = analysis.get_positive_reviews()
            negative_reviews = analysis.get_negative_reviews()
            sentiment_score = analysis.get_sentiment_score()
            
            print(f"\n📊 {analysis.name}:")
            print(f"   • Sentiment Score: {sentiment_score:.2f} (-1 to 1 scale)")
            print(f"   • Positive Reviews: {len(positive_reviews)}")
            print(f"   • Negative Reviews: {len(negative_reviews)}")
            
            if positive_reviews:
                print(f"   • Most Positive: \"{positive_reviews[0]['text'][:50]}...\"")
            if negative_reviews:
                print(f"   • Most Negative: \"{negative_reviews[0]['text'][:50]}...\"")

if __name__ == "__main__":
    main()