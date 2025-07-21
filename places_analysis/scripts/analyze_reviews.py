import pandas as pd
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

STOPWORDS = set(stopwords.words('english'))

def extract_keywords(reviews: list) -> list:
    """Extract simple keywords from reviews."""
    words = ' '.join(reviews).lower().split()
    return [w for w in words if w not in STOPWORDS]