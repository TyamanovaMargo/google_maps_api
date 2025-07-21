from pipeline.pipeline_runner import run_pipeline
from pipeline.save_results import save_to_csv, save_to_json, save_report
from scripts.visualize_data import (
    plot_ratings_distribution,
    plot_reviews_count_distribution,
    plot_price_level_distribution
)

if __name__ == "__main__":
    df, categories = run_pipeline('data/places_results.json')
    save_to_csv(df, 'reports/places_results.csv')
    save_to_json(df, 'reports/places_results.json')
    save_report("Top categories:\n" + str(categories.head(10)), 'reports/summary.txt')

    # Additional visualizations
    plot_ratings_distribution(df)
    plot_reviews_count_distribution(df)
    plot_price_level_distribution(df)

    print("✅ Analysis complete. Results saved in reports/ folder.")