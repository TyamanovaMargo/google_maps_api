import matplotlib.pyplot as plt
import seaborn as sns

def plot_top_categories(category_series, top_n=10):
    category_series.head(top_n).plot(kind='barh')
    plt.title('Top Categories')
    plt.xlabel('Count')
    plt.show()

def plot_ratings_distribution(df):
    plt.figure(figsize=(8, 5))
    sns.histplot(df['rating'].dropna(), bins=20, kde=True)
    plt.title('Ratings Distribution')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.show()

def plot_reviews_count_distribution(df):
    plt.figure(figsize=(8, 5))
    sns.histplot(df['user_ratings_total'].dropna(), bins=20, kde=False)
    plt.title('Reviews Count Distribution')
    plt.xlabel('Number of Reviews')
    plt.ylabel('Count of Places')
    plt.show()

def plot_price_level_distribution(df):
    plt.figure(figsize=(8, 5))
    sns.countplot(x='price_level', data=df)
    plt.title('Price Level Distribution')
    plt.xlabel('Price Level')
    plt.ylabel('Count of Places')
    plt.show()