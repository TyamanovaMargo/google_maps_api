import pandas as pd
import json

def save_to_csv(df: pd.DataFrame, path: str):
    """Save DataFrame to CSV."""
    df.to_csv(path, index=False)

def save_to_json(df: pd.DataFrame, path: str):
    """Save DataFrame to JSON."""
    df.to_json(path, orient='records', force_ascii=False, indent=2)

def save_report(text: str, path: str):
    """Save text report."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)