import json
import pandas as pd

def extract_places(json_path: str) -> pd.DataFrame:
    """
    Extract places information from Google Places API JSON.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    places = data.get('places', [])
    records = []
    for place in places:
        reviews = place.get('reviews', [])
        review_texts = [review.get('text', '') for review in reviews]
        records.append({
            'name': place.get('name'),
            'address': place.get('formatted_address') or place.get('vicinity'),
            'rating': place.get('rating'),
            'user_ratings_total': place.get('user_ratings_total'),
            'types': ", ".join(place.get('types', [])),
            'lat': place.get('latitude'),
            'lng': place.get('longitude'),
            'reviews': " ||| ".join(review_texts)
        })
    return pd.DataFrame(records)