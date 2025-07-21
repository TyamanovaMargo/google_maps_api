from scripts.extract_places import extract_places
from scripts.category_analysis import analyze_categories
from scripts.visualize_data import plot_top_categories

def run_pipeline(json_path: str):
    df = extract_places(json_path)
    categories = analyze_categories(df)
    plot_top_categories(categories)
    return df, categories