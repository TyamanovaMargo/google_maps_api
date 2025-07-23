#main.py
#!/usr/bin/env python3
"""
Business Places Analyzer - Main Entry Point
Analyzes business places using metadata and customer reviews
"""

import os
import sys
from typing import List
from dotenv import load_dotenv

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.loader import BusinessDataLoader
from src.analyzer import BusinessAnalyzer
from src.models import BusinessData, BusinessAnalysis
from src.utils import save_json, ensure_directories, setup_logging

# Load environment variables
load_dotenv()

logger = setup_logging()

class BusinessAnalysisOrchestrator:
    """Main orchestrator for business analysis workflow"""
    
    def __init__(self, data_file: str = "data/business_data.json"):
        self.data_file = data_file
        self.loader = BusinessDataLoader(data_file)
        self.analyzer = BusinessAnalyzer()
        self.businesses: List[BusinessData] = []
        self.analyses: List[BusinessAnalysis] = []
    
    def load_data(self) -> None:
        """Load business data"""
        logger.info("Loading business data...")
        self.businesses = self.loader.get_businesses()
        logger.info(f"Loaded {len(self.businesses)} businesses")
    
    def run_analysis(self) -> None:
        """Run comprehensive analysis on all businesses"""
        logger.info("Starting comprehensive business analysis...")
        self.analyses = self.analyzer.analyze_multiple_businesses(self.businesses)
        logger.info("Analysis completed")
    
    def save_results(self, output_file: str = "reports/analysis_output.json") -> None:
        """Save analysis results to JSON file"""
        logger.info(f"Saving results to {output_file}")
        
        # Convert to the required output format
        output_data = []
        for analysis in self.analyses:
            output_data.append({
                "name": analysis.name,
                "summary": analysis.summary,
                "recommendations": analysis.recommendations
            })
        
        save_json(output_data, output_file)
        logger.info(f"Results saved successfully to {output_file}")
    
    def run_interactive_queries(self) -> None:
        """Run sample queries to demonstrate functionality"""
        logger.info("Running sample queries...")
        
        sample_questions = [
            "What are the best-rated businesses?",
            "Which places have good service but low popularity?",
            "Are there frequent complaints about staff or delivery?",
            "Which businesses need the most improvement?"
        ]
        
        query_results = []
        for question in sample_questions:
            logger.info(f"Processing query: {question}")
            response = self.analyzer.query_businesses(question, self.businesses)
            query_results.append({
                "question": response.question,
                "answer": response.answer,
                "supporting_businesses": response.supporting_businesses
            })
        
        # Save query results
        save_json(query_results, "reports/query_results.json")
        logger.info("Query results saved to reports/query_results.json")
    
    def generate_summary_report(self) -> None:
        """Generate a summary report of all analyses"""
        if not self.analyses:
            logger.warning("No analyses available for summary report")
            return
        
        # Calculate summary statistics
        total_businesses = len(self.analyses)
        avg_rating = sum(b.rating for b in self.businesses) / total_businesses
        
        # Find top and bottom performers
        businesses_by_rating = sorted(self.businesses, key=lambda x: x.rating, reverse=True)
        top_rated = businesses_by_rating[:5]
        bottom_rated = businesses_by_rating[-5:]
        
        summary_report = {
            "total_businesses_analyzed": total_businesses,
            "average_rating": round(avg_rating, 2),
            "top_rated_businesses": [
                {"name": b.name, "rating": b.rating} for b in top_rated
            ],
            "businesses_needing_improvement": [
                {"name": b.name, "rating": b.rating} for b in bottom_rated
            ],
            "analysis_timestamp": "2025-07-23T10:00:00Z"
        }
        
        save_json(summary_report, "reports/summary_report.json")
        logger.info("Summary report saved to reports/summary_report.json")

def main():
    """Main execution function"""
    try:
        # Ensure required directories exist
        ensure_directories()
        
        # Initialize orchestrator
        orchestrator = BusinessAnalysisOrchestrator()
        
        # Check if data file exists
        if not os.path.exists(orchestrator.data_file):
            logger.error(f"Data file not found: {orchestrator.data_file}")
            logger.info("Please place your business data JSON file in the data/ directory")
            return
        
        # Run the complete analysis workflow
        orchestrator.load_data()
        orchestrator.run_analysis()
        orchestrator.save_results()
        orchestrator.run_interactive_queries()
        orchestrator.generate_summary_report()
        
        logger.info("Business analysis completed successfully!")
        logger.info("Check the reports/ directory for results:")
        logger.info("- analysis_output.json: Main analysis results")
        logger.info("- query_results.json: Sample query responses") 
        logger.info("- summary_report.json: Overall summary statistics")
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

