#  src/sentiment_utils.py
# """
# Utility functions for sentiment analysis operations
# """

from typing import List, Dict, Any, Tuple, Optional
import json
import re
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from .models import BusinessAnalysis, SentimentReport

class SentimentVisualizer:
    """Class for creating sentiment analysis visualizations"""
    
    @staticmethod
    def plot_sentiment_distribution(analyses: List[BusinessAnalysis], save_path: Optional[str] = None):
        """Create a pie chart of overall sentiment distribution"""
        sentiments = [analysis.overall_sentiment for analysis in analyses]
        sentiment_counts = Counter(sentiments)
        
        labels = list(sentiment_counts.keys())
        sizes = list(sentiment_counts.values())
        colors = {'positive': '#4CAF50', 'negative': '#F44336', 'neutral': '#FFC107'}
        plot_colors = [colors.get(label, '#9E9E9E') for label in labels]
        
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, colors=plot_colors, autopct='%1.1f%%', startangle=90)
        plt.title('Overall Sentiment Distribution')
        plt.axis('equal')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    @staticmethod
    def plot_business_sentiment_scores(analyses: List[BusinessAnalysis], save_path: Optional[str] = None):
        """Create a bar chart of sentiment scores for each business"""
        names = [analysis.name for analysis in analyses]
        scores = [analysis.get_sentiment_score() for analysis in analyses]
        colors = ['#4CAF50' if score > 0 else '#F44336' if score < 0 else '#FFC107' for score in scores]
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(names)), scores, color=colors)
        plt.xlabel('Businesses')
        plt.ylabel('Sentiment Score (-1 to 1)')
        plt.title('Business Sentiment Scores')
        plt.xticks(range(len(names)), names, rotation=45, ha='right')
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        plt.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + (0.02 if height >= 0 else -0.05),
                    f'{score:.2f}', ha='center', va='bottom' if height >= 0 else 'top')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    @staticmethod
    def plot_emotion_frequency(sentiment_report: SentimentReport, top_n: int = 10, save_path: Optional[str] = None):
        """Create a horizontal bar chart of emotion frequencies"""
        top_emotions = sentiment_report.top_emotions[:top_n]
        emotions = [e['emotion'] for e in top_emotions]
        frequencies = [e['frequency'] for e in top_emotions]
        
        plt.figure(figsize=(10, 6))
        bars = plt.barh(emotions, frequencies, color='#2196F3')
        plt.xlabel('Frequency')
        plt.ylabel('Emotions')
        plt.title(f'Top {top_n} Emotions in Customer Reviews')
        plt.gca().invert_yaxis()
        
        # Add value labels on bars
        for bar, freq in zip(bars, frequencies):
            width = bar.get_width()
            plt.text(width + 0.1, bar.get_y() + bar.get_height()/2,
                    str(freq), ha='left', va='center')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

class SentimentAnalyzer:
    """Advanced sentiment analysis utilities"""
    
    @staticmethod
    def calculate_sentiment_trends(analyses: List[BusinessAnalysis]) -> Dict[str, Any]:
        """Calculate sentiment trends and patterns"""
        total_businesses = len(analyses)
        
        # Calculate averages
        avg_positive = sum(a.sentiment_distribution['positive'] for a in analyses) / total_businesses
        avg_negative = sum(a.sentiment_distribution['negative'] for a in analyses) / total_businesses
        avg_neutral = sum(a.sentiment_distribution['neutral'] for a in analyses) / total_businesses
        
        # Find businesses with extreme sentiments
        most_positive = max(analyses, key=lambda a: a.get_sentiment_score())
        most_negative = min(analyses, key=lambda a: a.get_sentiment_score())
        
        # Calculate sentiment volatility (standard deviation of sentiment scores)
        sentiment_scores = [a.get_sentiment_score() for a in analyses]
        avg_score = sum(sentiment_scores) / len(sentiment_scores)
        volatility = (sum((score - avg_score) ** 2 for score in sentiment_scores) / len(sentiment_scores)) ** 0.5
        
        return {
            'average_sentiment_distribution': {
                'positive': round(avg_positive, 3),
                'negative': round(avg_negative, 3),
                'neutral': round(avg_neutral, 3)
            },
            'most_positive_business': {
                'name': most_positive.name,
                'score': most_positive.get_sentiment_score()
            },
            'most_negative_business': {
                'name': most_negative.name,
                'score': most_negative.get_sentiment_score()
            },
            'sentiment_volatility': round(volatility, 3),
            'overall_market_sentiment': 'positive' if avg_positive > max(avg_negative, avg_neutral) else 
                                      'negative' if avg_negative > avg_neutral else 'neutral'
        }
    
    @staticmethod
    def identify_sentiment_patterns(analyses: List[BusinessAnalysis]) -> Dict[str, List[str]]:
        """Identify businesses with similar sentiment patterns"""
        patterns = {
            'highly_positive': [],  # >70% positive
            'highly_negative': [],  # >50% negative
            'mixed_sentiment': [],  # Balanced positive/negative
            'neutral_dominant': [], # >60% neutral
            'polarized': []         # High positive AND high negative, low neutral
        }
        
        for analysis in analyses:
            dist = analysis.sentiment_distribution
            pos, neg, neu = dist['positive'], dist['negative'], dist['neutral']
            
            if pos > 0.7:
                patterns['highly_positive'].append(analysis.name)
            elif neg > 0.5:
                patterns['highly_negative'].append(analysis.name)
            elif neu > 0.6:
                patterns['neutral_dominant'].append(analysis.name)
            elif pos > 0.3 and neg > 0.3 and neu < 0.3:
                patterns['polarized'].append(analysis.name)
            else:
                patterns['mixed_sentiment'].append(analysis.name)
        
        return patterns
    
    @staticmethod
    def generate_sentiment_insights(analyses: List[BusinessAnalysis]) -> List[str]:
        """Generate actionable insights from sentiment analysis"""
        insights = []
        
        # Overall sentiment insight
        sentiment_report = aggregate_sentiment_data(analyses)
        pos_pct = sentiment_report.overall_sentiment_distribution['positive'] * 100
        neg_pct = sentiment_report.overall_sentiment_distribution['negative'] * 100
        
        if pos_pct > 60:
            insights.append(f"Market shows strong positive sentiment ({pos_pct:.1f}% positive)")
        elif neg_pct > 40:
            insights.append(f"Market shows concerning negative sentiment ({neg_pct:.1f}% negative)")
        
        # Identify outliers
        sentiment_scores = [(a.name, a.get_sentiment_score()) for a in analyses]
        sentiment_scores.sort(key=lambda x: x[1])
        
        if sentiment_scores:
            worst_performer = sentiment_scores[0]
            best_performer = sentiment_scores[-1]
            
            if worst_performer[1] < -0.3:
                insights.append(f"'{worst_performer[0]}' shows critically low sentiment (score: {worst_performer[1]:.2f})")
            
            if best_performer[1] > 0.5:
                insights.append(f"'{best_performer[0]}' demonstrates excellent customer sentiment (score: {best_performer[1]:.2f})")
        
        # Emotion-based insights
        all_emotions = []
        for analysis in analyses:
            all_emotions.extend(analysis.dominant_emotions)
        
        if all_emotions:
            emotion_counts = Counter(all_emotions)
            most_common = emotion_counts.most_common(3)
            
            if 'frustrated' in [emotion for emotion, _ in most_common]:
                insights.append("Customer frustration is a recurring theme across businesses")
            if 'satisfied' in [emotion for emotion, _ in most_common]:
                insights.append("Customer satisfaction levels are generally high")
        
        return insights

class SentimentReportGenerator:
    """Generate comprehensive sentiment analysis reports"""
    
    @staticmethod
    def generate_detailed_report(analyses: List[BusinessAnalysis]) -> str:
        """Generate a detailed text report of sentiment analysis"""
        if not analyses:
            return "No business analyses available for sentiment reporting."
        
        report = []
        report.append("=" * 60)
        report.append("COMPREHENSIVE SENTIMENT ANALYSIS REPORT")
        report.append("=" * 60)
        
        # Executive Summary
        sentiment_report = aggregate_sentiment_data(analyses)
        trends = SentimentAnalyzer.calculate_sentiment_trends(analyses)
        
        report.append(f"\n📊 EXECUTIVE SUMMARY")
        report.append(f"Total Businesses Analyzed: {len(analyses)}")
        report.append(f"Overall Market Sentiment: {trends['overall_market_sentiment'].upper()}")
        report.append(f"Sentiment Volatility: {trends['sentiment_volatility']:.3f}")
        
        dist = trends['average_sentiment_distribution']
        report.append(f"\nAverage Sentiment Distribution:")
        report.append(f"  • Positive: {dist['positive']:.1%}")
        report.append(f"  • Negative: {dist['negative']:.1%}")
        report.append(f"  • Neutral: {dist['neutral']:.1%}")
        
        # Top Performers
        report.append(f"\n🏆 PERFORMANCE HIGHLIGHTS")
        report.append(f"Best Sentiment: {trends['most_positive_business']['name']} ({trends['most_positive_business']['score']:.2f})")
        report.append(f"Worst Sentiment: {trends['most_negative_business']['name']} ({trends['most_negative_business']['score']:.2f})")
        
        # Emotion Analysis
        report.append(f"\n🎭 EMOTION ANALYSIS")
        top_emotions = sentiment_report.top_emotions[:5]
        for i, emotion_data in enumerate(top_emotions, 1):
            report.append(f"{i}. {emotion_data['emotion'].title()}: {emotion_data['frequency']} mentions")
        
        # Business Patterns
        patterns = SentimentAnalyzer.identify_sentiment_patterns(analyses)
        report.append(f"\n📈 SENTIMENT PATTERNS")
        for pattern, businesses in patterns.items():
            if businesses:
                report.append(f"{pattern.replace('_', ' ').title()}: {', '.join(businesses)}")
        
        # Individual Business Details
        report.append(f"\n🏢 INDIVIDUAL BUSINESS ANALYSIS")
        for analysis in sorted(analyses, key=lambda a: a.get_sentiment_score(), reverse=True):
            report.append(f"\n{analysis.name}")
            report.append(f"  Sentiment Score: {analysis.get_sentiment_score():.2f}")
            report.append(f"  Overall Sentiment: {analysis.overall_sentiment}")
            
            dist = analysis.sentiment_distribution
            report.append(f"  Distribution: {dist['positive']:.1%} pos, {dist['negative']:.1%} neg, {dist['neutral']:.1%} neu")
            
            if analysis.dominant_emotions:
                report.append(f"  Key Emotions: {', '.join(analysis.dominant_emotions[:3])}")
        
        # Actionable Insights
        insights = SentimentAnalyzer.generate_sentiment_insights(analyses)
        if insights:
            report.append(f"\n💡 KEY INSIGHTS & RECOMMENDATIONS")
            for i, insight in enumerate(insights, 1):
                report.append(f"{i}. {insight}")
        
        report.append(f"\n" + "=" * 60)
        report.append("END OF REPORT")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    @staticmethod
    def export_to_csv(analyses: List[BusinessAnalysis], filename: str):
        """Export sentiment analysis results to CSV"""
        data = []
        for analysis in analyses:
            dist = analysis.sentiment_distribution
            data.append({
                'business_name': analysis.name,
                'overall_sentiment': analysis.overall_sentiment,
                'sentiment_score': analysis.get_sentiment_score(),
                'positive_percentage': dist['positive'],
                'negative_percentage': dist['negative'],
                'neutral_percentage': dist['neutral'],
                'dominant_emotions': ', '.join(analysis.dominant_emotions),
                'total_reviews_analyzed': len(analysis.review_sentiments),
                'summary': analysis.summary
            })
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Sentiment analysis data exported to {filename}")

# Example usage functions
def quick_sentiment_overview(analyses: List[BusinessAnalysis]):
    """Print a quick overview of sentiment analysis results"""
    print("🔍 QUICK SENTIMENT OVERVIEW")
    print("-" * 40)
    
    for analysis in analyses:
        score = analysis.get_sentiment_score()
        emoji = "😊" if score > 0.2 else "😞" if score < -0.2 else "😐"
        print(f"{emoji} {analysis.name}: {score:.2f} ({analysis.overall_sentiment})")

def find_similar_sentiment_businesses(
    target_analysis: BusinessAnalysis, 
    all_analyses: List[BusinessAnalysis], 
    threshold: float = 0.2
) -> List[BusinessAnalysis]:
    """Find businesses with similar sentiment scores"""
    target_score = target_analysis.get_sentiment_score()
    similar = []
    
    for analysis in all_analyses:
        if analysis.name != target_analysis.name:
            score_diff = abs(analysis.get_sentiment_score() - target_score)
            if score_diff <= threshold:
                similar.append(analysis)
    
    return similar